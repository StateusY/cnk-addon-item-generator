execute \
        if data storage cnk:temp cooking_pot.Items[{id:"minecraft:porkchop"}] \
        if data storage cnk:temp cooking_pot.Items[{components:{"minecraft:custom_data":{spiced:{ingredient:{type:"any_grease"}}}}}] \
        if function cnk:cooking_pot/crafting/lock \
        run return run function spiced:cooking_pot/recipes/seared_sausage
execute \
        if data storage cnk:temp cooking_pot.Items[{id:"minecraft:porkchop"}] \
        if data storage cnk:temp cooking_pot.Items[{components:{"minecraft:custom_data":{spiced:{ingredient:{type:"any_grease"}}}}}] \
        if function cnk:cooking_pot/crafting/lock \
        run return run function spiced:cooking_pot/recipes/seared_sausage
