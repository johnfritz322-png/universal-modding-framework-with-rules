-- Forge Registry Probe — read-only.
--
-- Answers one question: after a plugin is mounted, does the live AssetRegistry
-- know about an asset that only exists inside that plugin?
--
-- It reads. It never grants, spawns, equips or writes to the game. The only
-- side effect is a text file next to this script.
--
-- Press F10 to run. Result lands in ForgeRegistryProbe/status.txt.

local PROBE_OBJECT = "/ForgeRegistryProbe/M_ForgeRegistryProbe0001.M_ForgeRegistryProbe0001"
local PROBE_PACKAGE = "/ForgeRegistryProbe/M_ForgeRegistryProbe0001"
-- A retail asset that is definitely registered, as a positive control. If the
-- control fails too, the probe itself is broken rather than the plugin route.
local CONTROL_PACKAGE = "/Game/_Dawnwalker/Inventory/Items/ITM_Weapon_SwordGreatMaster1a"

local function writeStatus(lines)
    local path = "ue4ss/Mods/ForgeRegistryProbe/status.txt"
    local f = io.open(path, "w")
    if not f then
        print("[ForgeRegistryProbe] could not open " .. path .. "\n")
        return
    end
    for _, l in ipairs(lines) do f:write(l .. "\n") end
    f:close()
    print("[ForgeRegistryProbe] wrote " .. path .. "\n")
end

local function getAssetRegistry()
    local helpers = StaticFindObject("/Script/AssetRegistry.Default__AssetRegistryHelpers")
    if not helpers or not helpers:IsValid() then return nil, "AssetRegistryHelpers not found" end
    local ok, reg = pcall(function() return helpers:GetAssetRegistry() end)
    if not ok or not reg or not reg:IsValid() then return nil, "GetAssetRegistry failed" end
    return reg, nil
end

local function packageKnown(reg, pkg)
    local ok, result = pcall(function()
        local assets = reg:GetAssetsByPackageName(FName(pkg), false, false)
        if assets and assets.Num then return assets:Num() end
        return 0
    end)
    if not ok then return -1 end
    return result or 0
end

local function run()
    local lines = { "ForgeRegistryProbe — " .. os.date("%Y-%m-%d %H:%M:%S") }

    local reg, err = getAssetRegistry()
    if not reg then
        lines[#lines + 1] = "RESULT=ERROR"
        lines[#lines + 1] = "reason=" .. tostring(err)
        writeStatus(lines)
        return
    end
    lines[#lines + 1] = "assetRegistry=ok"

    local control = packageKnown(reg, CONTROL_PACKAGE)
    local probe = packageKnown(reg, PROBE_PACKAGE)
    lines[#lines + 1] = "controlPackage=" .. CONTROL_PACKAGE
    lines[#lines + 1] = "controlAssets=" .. tostring(control)
    lines[#lines + 1] = "probePackage=" .. PROBE_PACKAGE
    lines[#lines + 1] = "probeAssets=" .. tostring(probe)

    local obj = StaticFindObject(PROBE_OBJECT)
    lines[#lines + 1] = "staticFindObject=" .. tostring(obj ~= nil and obj:IsValid())

    if control <= 0 then
        lines[#lines + 1] = "RESULT=PROBE_BROKEN"       -- control failed; test says nothing
    elseif probe > 0 then
        lines[#lines + 1] = "RESULT=REGISTERED"         -- plugin registry was appended
    else
        lines[#lines + 1] = "RESULT=NOT_REGISTERED"     -- mounting does not append
    end
    writeStatus(lines)
end

RegisterKeyBind(Key.F10, function()
    local ok, err = pcall(run)
    if not ok then print("[ForgeRegistryProbe] error: " .. tostring(err) .. "\n") end
end)

print("[ForgeRegistryProbe] loaded — press F10 to probe the asset registry\n")
