data modify storage cnk:temp cooking_pot.slot set from storage cnk:temp cooking_pot.Items[{id:"minecraft:porkchop"}].Slot
function cnk:recipes/remove with storage cnk:temp cooking_pot

data modify storage cnk:temp cooking_pot.slot set from storage cnk:temp cooking_pot.Items[{components:{"minecraft:custom_data":{spiced:{ingredient:{type:"any_grease"}}}}}].Slot
function cnk:recipes/remove with storage cnk:temp cooking_pot

# spawn the result
loot spawn ~ ~0.25 ~ loot spiced:food/seared_sausage

# MUST be called, handles animations/sounds and reset of data
function cnk:cooking_pot/effects/finish_cooking
