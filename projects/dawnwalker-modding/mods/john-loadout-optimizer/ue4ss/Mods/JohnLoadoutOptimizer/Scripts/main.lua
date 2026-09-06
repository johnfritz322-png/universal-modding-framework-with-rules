local MOD_NAME = "JohnLoadoutOptimizer"

-- These are numpad keys, not the top-row number keys.
local ATTACK_KEY = Key.NUM_ONE
local DEFENSE_KEY = Key.NUM_TWO

local SLOT_NAMES = {
    "Weapon",
    "OffHand",
    "Head",
    "Chest",
    "Hands",
    "Legs",
    "Feet",
    "Ring",
    "Ring2",
    "Amulet",
    "Amulet2",
}

local ATTACK_HINTS = {
    "damage",
    "attack",
    "dps",
    "critical",
    "crit",
    "weapon",
    "sword",
    "claw",
}

local DEFENSE_HINTS = {
    "defense",
    "defence",
    "armor",
    "armour",
    "resistance",
    "reduction",
    "health",
    "vitality",
    "chest",
    "head",
    "hands",
    "legs",
    "feet",
}

local function log(message)
    print(string.format("[%s] %s", MOD_NAME, message))
end

local function is_valid(value)
    if value == nil then
        return false
    end
    if type(value) == "userdata" or type(value) == "table" then
        local ok, result = pcall(function()
            if value.IsValid ~= nil then
                return value:IsValid()
            end
            return true
        end)
        return ok and result ~= false
    end
    return true
end

local function try(label, fn)
    local ok, result = pcall(fn)
    if not ok then
        log(label .. " failed: " .. tostring(result))
        return nil
    end
    return result
end

local function unwrap(value)
    if value == nil then
        return nil
    end
    if type(value) == "userdata" or type(value) == "table" then
        local ok, result = pcall(function()
            if value.get ~= nil then
                return value:get()
            end
            if value.Get ~= nil then
                return value:Get()
            end
            return value
        end)
        if ok then
            return result
        end
    end
    return value
end

local function to_text(value)
    if value == nil then
        return ""
    end
    local ok, result = pcall(function()
        if type(value) == "userdata" or type(value) == "table" then
            if value.GetFullName ~= nil then
                return value:GetFullName()
            end
            if value.GetName ~= nil then
                return value:GetName()
            end
        end
        return tostring(value)
    end)
    if ok and result ~= nil then
        return tostring(result)
    end
    return tostring(value)
end

local function find_player()
    local names = {
        "DawnwalkerPlayerCharacter",
        "DawnwalkerCharacterBase",
        "PlayerCharacter",
    }
    for _, name in ipairs(names) do
        local player = try("FindFirstOf(" .. name .. ")", function()
            return FindFirstOf(name)
        end)
        if is_valid(player) then
            log("Using player object: " .. to_text(player))
            return player
        end
    end
    return nil
end

local function find_inventory(player)
    if not is_valid(player) then
        return nil
    end

    local inventory = try("player:GetInventoryComponent()", function()
        return player:GetInventoryComponent()
    end)
    if is_valid(inventory) then
        log("Using inventory from player:GetInventoryComponent()")
        return inventory
    end

    local subsystem = try("FindFirstOf(InventorySubsystem)", function()
        return FindFirstOf("InventorySubsystem")
    end)
    if is_valid(subsystem) then
        inventory = try("InventorySubsystem:GetPlayerInventoryComponent()", function()
            return subsystem:GetPlayerInventoryComponent()
        end)
        if is_valid(inventory) then
            log("Using inventory from InventorySubsystem")
            return inventory
        end
    end

    inventory = try("FindFirstOf(InventoryComponent)", function()
        return FindFirstOf("InventoryComponent")
    end)
    if is_valid(inventory) then
        log("Using first InventoryComponent as fallback")
        return inventory
    end

    return nil
end

local function each_array(array, callback)
    if array == nil then
        return 0
    end

    local count = 0
    if type(array) == "table" or type(array) == "userdata" then
        local has_for_each = try("array.ForEach probe", function()
            return array.ForEach ~= nil
        end)
        if has_for_each then
            try("array:ForEach", function()
                array:ForEach(function(index, elem)
                    local item = unwrap(elem)
                    count = count + 1
                    callback(index, item)
                end)
            end)
            return count
        end

        local n = try("array:GetArrayNum()", function()
            return array:GetArrayNum()
        end)
        if type(n) == "number" then
            for i = 0, n - 1 do
                local item = unwrap(array[i])
                if item ~= nil then
                    count = count + 1
                    callback(i, item)
                end
            end
            return count
        end

        local len = try("#array", function()
            return #array
        end)
        if type(len) == "number" then
            for i = 1, len do
                local item = unwrap(array[i])
                if item ~= nil then
                    count = count + 1
                    callback(i, item)
                end
            end
        end
    end

    return count
end

local function get_number(value)
    value = unwrap(value)
    if type(value) == "number" then
        return value
    end
    if type(value) == "userdata" or type(value) == "table" then
        for _, method in ipairs({ "Get", "get", "ToNumber" }) do
            local ok, result = pcall(function()
                return value[method](value)
            end)
            if ok and type(result) == "number" then
                return result
            end
        end
    end
    local numeric = tonumber(value)
    if numeric ~= nil then
        return numeric
    end
    return 0
end

local function get_asset(item)
    if not is_valid(item) then
        return nil
    end

    for _, field in ipairs({ "ItemAsset", "Asset", "DataAsset", "ItemData", "Item", "Definition" }) do
        local asset = try("item." .. field, function()
            return item[field]
        end)
        asset = unwrap(asset)
        if is_valid(asset) then
            return asset
        end
    end

    return item
end

local function score_by_methods(item, mode)
    local asset = get_asset(item)
    local score = 0

    if is_valid(asset) then
        if mode == "attack" then
            score = math.max(score, get_number(try("GetDamagePerSecond", function()
                return asset:GetDamagePerSecond()
            end)))
            score = math.max(score, get_number(try("GetWeaponDamage", function()
                return asset:GetWeaponDamage()
            end)))
        else
            score = math.max(score, get_number(try("GetItemProperty(ArmorPhysicalDamageReductionValue)", function()
                return asset:GetItemProperty(FName("ArmorPhysicalDamageReductionValue"))
            end)))
            score = math.max(score, get_number(try("GetItemProperty(Defense)", function()
                return asset:GetItemProperty(FName("Defense"))
            end)))
        end
    end

    return score
end

local function score_by_name(item, mode)
    local text = string.lower(to_text(item) .. " " .. to_text(get_asset(item)))
    local hints = mode == "attack" and ATTACK_HINTS or DEFENSE_HINTS
    local score = 0
    for _, hint in ipairs(hints) do
        if string.find(text, hint, 1, true) then
            score = score + 1
        end
    end
    return score
end

local function score_item(item, mode)
    return (score_by_methods(item, mode) * 1000) + score_by_name(item, mode)
end

local function slot_accepts_item(inventory, item, slot_name)
    local valid_slots = try("GetValidEquipmentSlotsForItem", function()
        return inventory:GetValidEquipmentSlotsForItem(item)
    end)
    if valid_slots == nil then
        return true
    end

    local wanted = string.lower(slot_name)
    local accepts = false
    each_array(valid_slots, function(_, slot)
        if string.find(string.lower(to_text(slot)), wanted, 1, true) then
            accepts = true
        end
    end)
    return accepts
end

local function equip_item(inventory, item, slot_name)
    local result = try("TryEquipItemInSlot(" .. slot_name .. ")", function()
        return inventory:TryEquipItemInSlot(item, FName(slot_name))
    end)
    if result ~= nil then
        return result
    end

    return try("TryEquipItem", function()
        return inventory:TryEquipItem(item)
    end)
end

local function optimize(mode)
    log("Optimize " .. mode .. " requested")

    local player = find_player()
    local inventory = find_inventory(player)
    if not is_valid(inventory) then
        log("No usable inventory component found.")
        return
    end

    local items = try("inventory:GetCurrentItems()", function()
        return inventory:GetCurrentItems()
    end)
    if items == nil then
        log("GetCurrentItems returned nil.")
        return
    end

    local best_by_slot = {}
    local total = each_array(items, function(_, item)
        if is_valid(item) then
            for _, slot_name in ipairs(SLOT_NAMES) do
                if slot_accepts_item(inventory, item, slot_name) then
                    local score = score_item(item, mode)
                    local best = best_by_slot[slot_name]
                    if score > 0 and (best == nil or score > best.score) then
                        best_by_slot[slot_name] = {
                            item = item,
                            score = score,
                            text = to_text(item),
                        }
                    end
                end
            end
        end
    end)

    log("Scanned " .. tostring(total) .. " inventory entries.")

    local equipped = 0
    for _, slot_name in ipairs(SLOT_NAMES) do
        local best = best_by_slot[slot_name]
        if best ~= nil then
            local result = equip_item(inventory, best.item, slot_name)
            equipped = equipped + 1
            log(string.format("%s -> score %.2f -> %s -> %s", slot_name, best.score, best.text, tostring(result)))
        end
    end

    log("Optimize " .. mode .. " finished. Attempted equips: " .. tostring(equipped))
end

RegisterKeyBind(ATTACK_KEY, function()
    ExecuteInGameThread(function()
        optimize("attack")
    end)
end)

RegisterKeyBind(DEFENSE_KEY, function()
    ExecuteInGameThread(function()
        optimize("defense")
    end)
end)

log("Loaded. Numpad 1 = optimize attack. Numpad 2 = optimize defense.")
