-- Forge Registry Probe — read-only.
--
-- Question: after a plugin is mounted, can the game load and see an asset that
-- exists only inside that plugin?
--
-- Reads only. Never grants, spawns, equips, or writes to a save. The single
-- side effect is one text file next to this script.
--
-- Press F8. Result: ForgeRegistryProbe/status.txt
--
-- Notes from earlier runs, kept so they are not rediscovered:
--   * Not F10 - ForgeItemLoadProbe and ConsoleEnabler both bind it.
--   * Forward slashes in paths - Lua has no escape trap there, "D:\s" does.
--   * LoadAsset and the asset-registry calls must run on the GAME THREAD, or
--     they throw "can only be called from within the game". Hence
--     ExecuteInGameThread around everything.

local PROBE_OBJ = "/ForgeRegistryProbe/M_ForgeRegistryProbe0001.M_ForgeRegistryProbe0001"
local CTRL_OBJ  = "/Game/_Dawnwalker/Inventory/Items/ITM_Weapon_SwordGreatMaster1a.ITM_Weapon_SwordGreatMaster1a"
local STATUS    = "D:/steam/steamapps/common/The Blood of Dawnwalker/Dawnwalker/Binaries/Win64/ue4ss/Mods/ForgeRegistryProbe/status.txt"

local out = {}
local function say(s) out[#out + 1] = s end

local function findState(path)
    local ok, obj = pcall(StaticFindObject, path)
    if not ok or obj == nil then return "absent" end
    local okv, valid = pcall(function() return obj:IsValid() end)
    return (okv and valid) and "present" or "absent"
end

local function probeOne(label, path)
    say("[" .. label .. "] " .. path)
    say("  beforeLoad=" .. findState(path))
    local ok, err = pcall(function() return LoadAsset(path) end)
    if ok then
        say("  loadAsset=ok")
    else
        say("  loadAsset=threw: " .. tostring(err):sub(1, 70))
    end
    say("  afterLoad=" .. findState(path))
end

local function run()
    out = {}
    say("ForgeRegistryProbe — " .. os.date("%Y-%m-%d %H:%M:%S"))
    say("(LoadAsset pulls the asset in if the game can resolve it at all;")
    say(" afterLoad=present means the plugin content is reachable.)")
    say("")
    probeOne("control", CTRL_OBJ)
    say("")
    probeOne("probe", PROBE_OBJ)
    say("")

    local before = nil
    for _, l in ipairs(out) do
        if l:find("%[probe%]") then before = true end
    end
    -- verdict from the probe's afterLoad line
    local verdict = "UNCLEAR"
    for i, l in ipairs(out) do
        if l == "[probe] " .. PROBE_OBJ then
            local after = out[i + 3] or ""
            if after:find("present") then verdict = "PLUGIN_CONTENT_REACHABLE"
            else verdict = "PLUGIN_CONTENT_NOT_REACHABLE" end
        end
    end
    say("RESULT=" .. verdict)

    local f = io.open(STATUS, "w")
    if f then
        for _, l in ipairs(out) do f:write(l .. "\n") end
        f:close()
        print("[ForgeRegistryProbe] wrote status.txt\n")
    else
        print("[ForgeRegistryProbe] could not write status.txt\n")
    end
end

RegisterKeyBind(Key.F8, function()
    -- everything that touches UObjects must be on the game thread
    ExecuteInGameThread(function()
        local ok, err = pcall(run)
        if not ok then print("[ForgeRegistryProbe] error: " .. tostring(err) .. "\n") end
    end)
end)

print("[ForgeRegistryProbe] loaded — press F8 to probe\n")
