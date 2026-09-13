-- Test-only Dawnwalker Weapon Forge probe.
-- F10 asks the running game to load exactly one additive test item package.
-- It does not grant an item, modify a save, or replace a retail weapon.

local assetPath = "/Game/_Dawnwalker/Inventory/Items/ITM_Weapon_ForgeTestSword0000"
local objectPath = assetPath .. ".ITM_Weapon_ForgeTestSword0000"

local function valid(object)
    return object and object:IsValid()
end

RegisterKeyBind(Key.F10, function()
    ExecuteInGameThread(function()
        for _, path in ipairs({assetPath, objectPath}) do
            print("[ForgeItemLoadProbe] Loading " .. path .. "\n")
            local ok, err = pcall(function()
                LoadAsset(path)
            end)
            if not ok then
                print("[ForgeItemLoadProbe] LoadAsset error: " .. tostring(err) .. "\n")
            else
                local item = StaticFindObject(objectPath)
                if valid(item) then
                    print("[ForgeItemLoadProbe] LOADED " .. item:GetFullName() .. "\n")
                    return
                end
                print("[ForgeItemLoadProbe] NOT_FOUND after LoadAsset\n")
            end
        end
    end)
end)

print("[ForgeItemLoadProbe] Ready: F10 loads the test item only; no inventory change.\n")
