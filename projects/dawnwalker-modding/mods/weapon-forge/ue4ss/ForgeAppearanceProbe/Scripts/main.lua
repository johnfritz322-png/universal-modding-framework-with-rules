-- Forge Appearance Probe — read-only.
--
-- Question: when the appearance table is overridden, does the game use the
-- override? Answers it three independent ways so one broken method cannot be
-- mistaken for a real result.
--
-- Reads only. Never grants, spawns, equips, or writes to a save. The single side
-- effect is one text file next to this script.
--
-- Press F8 while IN GAME with the weapon under test EQUIPPED.
-- Result: ForgeAppearanceProbe/status.txt
--
-- Conventions learned the hard way on this project - keep them:
--   * F8, not F10. ForgeItemLoadProbe and ConsoleEnabler both bind F10.
--   * Forward slashes in paths. A backslash path is an invalid Lua escape and
--     kills the whole script at load, silently binding nothing.
--   * Anything touching UObjects must run inside ExecuteInGameThread, or it
--     throws "can only be called from within the game".
--   * unreal.log / print do NOT reliably reach the log. Write to a file.

local STATUS = "D:/steam/steamapps/common/The Blood of Dawnwalker/Dawnwalker/Binaries/Win64/ue4ss/Mods/ForgeAppearanceProbe/status.txt"

-- The item under test and the two candidate blades.
local TABLE_PATH   = "/Game/_Dawnwalker/Inventory/Items/DT_WeaponAppearances"
local ROW_NAME     = "ITM_Weapon_SwordVampiric1a"
local ORIGINAL     = "L_Sword_Vampiric_01"        -- what the unmodified table says
local OVERRIDDEN   = "M_Sword_Gargoyle_01"        -- what our patched table says
-- Control: a row nobody modified. If this reads wrong, the probe is broken.
local CTRL_ROW     = "ITM_Weapon_SwordErkas1a"
local CTRL_EXPECT  = "M_Sword_Erka_01"

local out = {}
local function say(s) out[#out + 1] = tostring(s) end

local function objName(o)
    if o == nil then return "nil" end
    local ok, n = pcall(function() return o:GetFullName() end)
    if ok and n then return tostring(n) end
    return "<unnamed>"
end

local function isLoaded(shortName)
    -- StaticFindObject only sees what is already in memory, so a miss here is
    -- not proof of absence - it is only meaningful alongside the other checks.
    local p = "/Game/_Dawnwalker/Characters/Swords/" .. shortName .. "/" .. shortName
                .. "." .. shortName
    local ok, o = pcall(StaticFindObject, p)
    if not ok or o == nil then return false end
    local okv, v = pcall(function() return o:IsValid() end)
    return okv and v
end

-- 1. What mesh is actually rendering on the equipped weapon.
local function probeEquippedMesh()
    say("")
    say("[1] equipped weapon's live mesh")
    local pc = UEHelpers and UEHelpers.GetPlayerController and UEHelpers.GetPlayerController()
    if pc == nil or not pc:IsValid() then
        local ok, found = pcall(function()
            return FindFirstOf("PlayerController")
        end)
        pc = (ok and found) or nil
    end
    if pc == nil or not pc:IsValid() then
        say("  playerController=not found (load a save and be in game)")
        return
    end
    say("  playerController=ok")

    -- Every StaticMeshComponent currently alive whose mesh is one of the sword
    -- assets. This finds the equipped blade without needing the exact component
    -- path, which differs per weapon blueprint.
    local hits = {}
    local ok = pcall(function()
        local comps = FindAllOf("StaticMeshComponent") or {}
        for _, c in ipairs(comps) do
            if c and c:IsValid() then
                local okm, m = pcall(function() return c.StaticMesh end)
                if okm and m and m:IsValid() then
                    local n = objName(m)
                    if n:find("Characters/Swords") or n:find("_Sword_") then
                        hits[#hits + 1] = n
                    end
                end
            end
        end
    end)
    if not ok then
        say("  component scan threw")
        return
    end
    if #hits == 0 then
        say("  no sword StaticMeshComponent found — is the weapon drawn/equipped?")
    end
    for i = 1, math.min(#hits, 12) do say("  mesh: " .. hits[i]) end
end

-- 2. Which candidate blade packages are resident.
local function probeResident()
    say("")
    say("[2] which candidate blades are loaded in memory")
    say("  " .. ORIGINAL .. " loaded=" .. tostring(isLoaded(ORIGINAL)))
    say("  " .. OVERRIDDEN .. " loaded=" .. tostring(isLoaded(OVERRIDDEN)))
    say("  (" .. OVERRIDDEN .. "=true is strong evidence the override is live)")
end

-- 3. The appearance table object itself, and whether our row exists in it.
local function probeTable()
    say("")
    say("[3] appearance table")
    local ok, tbl = pcall(StaticFindObject, TABLE_PATH .. "." .. "DT_WeaponAppearances")
    if not ok or tbl == nil or not tbl:IsValid() then
        say("  table not resident — it may load on demand; this is not conclusive")
        return
    end
    say("  table=" .. objName(tbl))
    local okn, names = pcall(function()
        return UDataTableFunctionLibrary:GetDataTableRowNames(tbl)
    end)
    if not okn or names == nil then
        say("  GetDataTableRowNames unavailable (needs a struct-aware call)")
        say("  rows cannot be read from Lua directly; rely on [1] and [2]")
        return
    end
    local count, found, ctrl = 0, false, false
    for _, n in ipairs(names) do
        count = count + 1
        local s = tostring(n)
        if s == ROW_NAME then found = true end
        if s == CTRL_ROW then ctrl = true end
    end
    say("  rowCount=" .. count)
    say("  hasRow(" .. ROW_NAME .. ")=" .. tostring(found))
    say("  hasControlRow(" .. CTRL_ROW .. ")=" .. tostring(ctrl))
end

local function verdict()
    say("")
    if isLoaded(OVERRIDDEN) then
        say("VERDICT=OVERRIDE_LIVE — our container is winning; the visual comes")
        say("  from somewhere other than this table. Look at the equip path and")
        say("  AppearanceSubsystem.ItemAppearanceMap.")
    elseif isLoaded(ORIGINAL) then
        say("VERDICT=ORIGINAL_IN_USE — the game is using the stock blade, so our")
        say("  container is probably not winning. Check load order and packaging.")
    else
        say("VERDICT=INCONCLUSIVE — neither blade is resident. Equip the weapon,")
        say("  make sure it is drawn, then press F8 again.")
    end
end

local function run()
    out = {}
    say("ForgeAppearanceProbe — " .. os.date("%Y-%m-%d %H:%M:%S"))
    say("item=" .. ROW_NAME)
    say("original=" .. ORIGINAL .. "  overridden=" .. OVERRIDDEN)
    say("control row=" .. CTRL_ROW .. " expects " .. CTRL_EXPECT)
    probeEquippedMesh()
    probeResident()
    probeTable()
    verdict()

    local f = io.open(STATUS, "w")
    if f then
        for _, l in ipairs(out) do f:write(l .. "\n") end
        f:close()
        print("[ForgeAppearanceProbe] wrote status.txt\n")
    else
        print("[ForgeAppearanceProbe] could not write status.txt\n")
    end
end

RegisterKeyBind(Key.F8, function()
    ExecuteInGameThread(function()
        local ok, err = pcall(run)
        if not ok then print("[ForgeAppearanceProbe] error: " .. tostring(err) .. "\n") end
    end)
end)

print("[ForgeAppearanceProbe] loaded — equip the weapon, then press F8\n")
