-- Forge Appearance Probe — read-only.
--
-- Checks a SET of weapon visual overrides: for each, is the overridden blade
-- held by the player, or is the original still in use?
--
-- Reads only. Never grants, spawns, equips, or writes to a save. One text file
-- is its only side effect.
--
-- Press F8 with the weapon DRAWN. Sheathed gives INCONCLUSIVE, correctly.
-- Result: ForgeAppearanceProbe/status.txt
--
-- Conventions, each learned by losing a run — keep them:
--   * F8, not F10 (ForgeItemLoadProbe and ConsoleEnabler both bind F10).
--   * Forward slashes in paths. A Windows path is an invalid Lua escape and
--     kills the script at load, silently binding nothing.
--   * ExecuteInGameThread around anything touching UObjects.
--   * Write results to a FILE; print does not reliably reach the log.
--   * Compare owners by OBJECT IDENTITY, not name — a second
--     BP_PlayerCharacter_C exists inside a cutscene, so names collide.
--   * UE4SS loads Lua at startup only: editing this needs a game restart.

local STATUS = "D:/steam/steamapps/common/The Blood of Dawnwalker/Dawnwalker/Binaries/Win64/ue4ss/Mods/ForgeAppearanceProbe/status.txt"

-- label, stock blade, blade we repointed it to
local SET = {
    { "The Vrakhir",              "L_Sword_Vampiric_01",   "M_Sword_Ancient_Hero_01" },
    { "Imbued Sword of St Mihai", "S_Sword_Dawnwalker_01", "M_Sword_Matron_01"       },
    { "Sword Great Master 1a",    "L_Sword_NPC_07",        "M_Sword_Skender_01"      },
}

local out = {}
local function say(s) out[#out + 1] = tostring(s) end

local function objName(o)
    if o == nil then return "nil" end
    local ok, n = pcall(function() return o:GetFullName() end)
    return (ok and n) and tostring(n) or "<unnamed>"
end

local function isLoaded(short)
    local p = "/Game/_Dawnwalker/Characters/Swords/" .. short .. "/" .. short .. "." .. short
    local ok, o = pcall(StaticFindObject, p)
    if not ok or o == nil then return false end
    local okv, v = pcall(function() return o:IsValid() end)
    return okv and v
end

local function sameObject(a, b)
    if a == nil or b == nil then return false, "none" end
    local ok, eq = pcall(function() return a == b end)
    if ok and eq then return true, "object-identity" end
    local oka, x = pcall(function() return a:GetAddress() end)
    local okb, y = pcall(function() return b:GetAddress() end)
    if oka and okb and x ~= nil and x == y then return true, "address" end
    return false, "none"
end

local function run()
    out = {}
    say("ForgeAppearanceProbe — " .. os.date("%Y-%m-%d %H:%M:%S"))
    say("VISUAL REPLACEMENT of existing weapons. Does NOT create new items.")
    say("")

    local pawn = nil
    pcall(function()
        local pc = FindFirstOf("PlayerController")
        if pc and pc:IsValid() then pawn = pc.Pawn end
    end)
    say("player pawn = " .. (pawn and objName(pawn) or "NOT FOUND"))

    -- one scan of the world, reused for every weapon in the set
    local held = {}          -- short mesh name -> { onPlayer=bool, how=string }
    pcall(function()
        local comps = FindAllOf("StaticMeshComponent") or {}
        say("StaticMeshComponents alive: " .. tostring(#comps))
        for _, c in ipairs(comps) do
            if c and c:IsValid() then
                local okm, m = pcall(function() return c.StaticMesh end)
                if okm and m and m:IsValid() then
                    local mn = objName(m)
                    local short = mn:match("Characters/Swords/[^/]+/([^/.]+)%.")
                    if short then
                        local oko, owner = pcall(function() return c:GetOuter() end)
                        local onPlayer, how = false, "none"
                        if oko then onPlayer, how = sameObject(owner, pawn) end
                        local e = held[short]
                        if e == nil then
                            held[short] = { onPlayer = onPlayer, how = how }
                        elseif onPlayer and not e.onPlayer then
                            e.onPlayer, e.how = true, how
                        end
                    end
                end
            end
        end
    end)

    local pass, fail, unclear = 0, 0, 0
    for _, row in ipairs(SET) do
        local label, stock, want = row[1], row[2], row[3]
        say("")
        say("[" .. label .. "]  " .. stock .. " -> " .. want)
        local w, s = held[want], held[stock]
        say("  overridden resident=" .. tostring(isLoaded(want))
            .. "  held=" .. tostring(w ~= nil)
            .. "  onPlayer=" .. tostring(w ~= nil and w.onPlayer or false)
            .. (w and ("  (via " .. w.how .. ")") or ""))
        say("  stock      resident=" .. tostring(isLoaded(stock))
            .. "  held=" .. tostring(s ~= nil)
            .. "  onPlayer=" .. tostring(s ~= nil and s.onPlayer or false))
        if w ~= nil and w.onPlayer then
            say("  => OVERRIDE_ON_PLAYER"); pass = pass + 1
        elseif s ~= nil and s.onPlayer then
            say("  => STOCK_ON_PLAYER — override not applied to this weapon"); fail = fail + 1
        else
            say("  => INCONCLUSIVE — not equipped/drawn right now"); unclear = unclear + 1
        end
    end

    say("")
    say("SUMMARY  confirmed=" .. pass .. "  stock-still-showing=" .. fail
        .. "  not-tested=" .. unclear)
    say("Equip and DRAW each weapon in turn, pressing F8 for each, to confirm all three.")

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

print("[ForgeAppearanceProbe] loaded — draw a weapon, then press F8\n")
