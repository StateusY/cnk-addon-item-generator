execute if score $mortar_and_pestle_item_count cnk.dummy matches 5 \
        if data storage cnk:temp mortar_and_pestle.Items[{components:{"minecraft:custom_data":{spiced:{ingredient:{type:"rosemary"}}}}}] \
        if data storage cnk:temp mortar_and_pestle.Items[{components:{"minecraft:custom_data":{spiced:{ingredient:{type:"thyme"}}}}}] \
        if data storage cnk:temp mortar_and_pestle.Items[{components:{"minecraft:custom_data":{spiced:{ingredient:{type:"oregano"}}}}}] \
        if data storage cnk:temp mortar_and_pestle.Items[{components:{"minecraft:custom_data":{spiced:{ingredient:{type:"marjoram"}}}}}] \
        if data storage cnk:temp mortar_and_pestle.Items[{components:{"minecraft:custom_data":{spiced:{ingredient:{type:"basil"}}}}}] \
        if function spiced:mortar_and_pestle/mash/lock \
        run return run data modify entity @s item.components."minecraft:custom_data".spiced.mash_callback set value "spiced:recipes/mortar_and_pestle/cajun_seasoning"
execute if score $mortar_and_pestle_item_count cnk.dummy matches 5 \
        if data storage cnk:temp mortar_and_pestle.Items[{components:{"minecraft:custom_data":{spiced:{ingredient:{type:"rosemary"}}}}}] \
        if data storage cnk:temp mortar_and_pestle.Items[{components:{"minecraft:custom_data":{spiced:{ingredient:{type:"thyme"}}}}}] \
        if data storage cnk:temp mortar_and_pestle.Items[{components:{"minecraft:custom_data":{spiced:{ingredient:{type:"oregano"}}}}}] \
        if data storage cnk:temp mortar_and_pestle.Items[{components:{"minecraft:custom_data":{spiced:{ingredient:{type:"marjoram"}}}}}] \
        if data storage cnk:temp mortar_and_pestle.Items[{components:{"minecraft:custom_data":{spiced:{ingredient:{type:"basil"}}}}}] \
        if function spiced:mortar_and_pestle/mash/lock \
        run return run data modify entity @s item.components."minecraft:custom_data".spiced.mash_callback set value "spiced:recipes/mortar_and_pestle/cajun_seasoning"
