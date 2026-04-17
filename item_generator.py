import csv
import json
from pathlib import Path
from collections import defaultdict

lang_entries = defaultdict(dict)       # {namespace: {key: name}}
icon_entries = defaultdict(list)       # {namespace: [provider, ...]}
icon_counters = defaultdict(lambda: 1) # {namespace: next_char_index}

csv_offset = 10

# helper functions
def to_int(value):
    try:
        return int(float(value)) 
    except (ValueError, TypeError):
        return 0
def to_float(value):
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0
def write_to_file(path, file, data, i, write_style="w"):
    if do_dynamic_insertion:
        if pack_directory == "within":
            directory = Path(path)
        else:
            directory = Path(f"{data_array[i+csv_offset][1]}/{path}")
    directory.mkdir(parents=True, exist_ok=True)
    file_path = directory / file

    backup_file(file_path)

    with open(file_path, write_style, encoding="utf-8") as f:
        if type(data) is dict:
            json.dump(data, f, indent=4)
        elif type(data) is list:
            f.writelines(data)
def backup_file(file_path):
    file_path = Path(file_path)
    if do_backups and file_path.exists():
        stem = file_path.stem
        ext = file_path.suffix
        backup_path = file_path.parent / f"bak_{file_path.name}"
        if backup_path.exists():
            counter = 2
            while backup_path.exists():
                backup_path = file_path.parent / f"bak{counter}_{stem}{ext}"
                counter += 1
        file_path.rename(backup_path)
        
# read csv
with open('data.csv', newline='') as f:
    reader = csv.reader(f)
    # convert reader into a list
    data_array = list(reader)

do_dynamic_insertion = data_array[2][1].lower() == "true"
do_backups = data_array[2][2].lower() == "true"
pack_directory = data_array[2][3].lower()


# find workstations
worklstation_list = list(set(data_array[i+csv_offset][9] for i in range(len(data_array)-10)))
worklstation_list = [x for x in worklstation_list if x]
# pages
cookbook_groups = ["staple", "snacks", "light", "hearty", "feasts", "deserts"]
cookbook_pages = [[], [], [], [], [], []]
distiller_pages = []


for i in range(len(data_array)-10):

    namespace = data_array[i+csv_offset][1]
    item_id   = data_array[i+csv_offset][2]
    item_name = data_array[i+csv_offset][3]
    
    # icons
    
    char_index = icon_counters[namespace]
    char = f"\\ud{char_index:03d}"  # \ud001, \ud002, etc.
    icon_entries[namespace].append({
        "type": "bitmap",
        "file": f"{namespace}:icon/item/{item_id}.png",
        "ascent": 15,
        "height": 16,
        "chars": [char]
    })
    icon_counters[namespace] += 1
    # lang
    char = chr(0xD000 + char_index)
    lang_entries[namespace][f"item.{namespace}.{item_id}"] = item_name
    lang_entries[namespace][f"book.item.{namespace}.{item_id}"] = char

    # model files
    model = {
        "parent": "minecraft:item/generated",
        "textures": {
            "layer0": f"{data_array[i+csv_offset][1]}:item/{data_array[i+csv_offset][2]}"
        }
    }
    write_to_file(f"assets/{data_array[i+csv_offset][1]}/models/item",f"{data_array[i+10][2]}.json",model,i,"w")

    # item files
    item = {
        "model": {
            "type": "minecraft:model",
            "model": f"{data_array[i+csv_offset][1]}:item/{data_array[i+csv_offset][2]}"
        }
    }
    write_to_file(f"assets/{data_array[i+csv_offset][1]}/items",f"{data_array[i+10][2]}.json",item,i,"w")

    # advancements
    item = {
        "parent": "cnk:cookbook/root",
        "criteria": {
            "requirement": {
            "trigger": "minecraft:inventory_changed",
            "conditions": {
                "items": [
                {
                    "items": "minecraft:poisonous_potato",
                    "predicates": {
                    "minecraft:custom_data": {f"{data_array[i+csv_offset][1]}":{"ingredient":{"type":f"{data_array[i+csv_offset][2]}"}}}
                    }
                }
                ]
            }
            }
        },
        "rewards": {
            "function": f"{data_array[i+csv_offset][1]}:cookbook/grant/{data_array[i+csv_offset][2]}"
        }
    }
    write_to_file(f"data/{data_array[i+csv_offset][1]}/advancement/cookbook/{data_array[i+csv_offset][2]}","item.json",item,i,"w")

    toast = {
        "parent": "cnk:cookbook/toasts",
        "display": {
            "title": [{"translate":"book.cnk.toast.background","font":"cnk.book:advancement"},{"translate":f"book.cnk.toast.unlock.{data_array[i+csv_offset][4]}","font":"cnk.book:advancement_text","color":"#7b613a"}],
            "icon": {
            "id": "minecraft:poisonous_potato",
            "components": {"minecraft:item_model": f"{data_array[i+csv_offset][1]}:{data_array[i+csv_offset][2]}"}
            },
            "description": "",
            "announce_to_chat": False
        },
        "criteria": {
            "requirement": {
            "trigger": "minecraft:impossible"
            }
        }
    }
    write_to_file(f"data/{data_array[i+csv_offset][1]}/advancement/cookbook/{data_array[i+csv_offset][2]}","toast.json",toast,i,"w")
    

    # loot tables
    if data_array[i+csv_offset][16] != "TRUE":
        loot = {
            "pools": [
                {
                "rolls": 1,
                "entries": [
                    {
                    "type": "minecraft:item",
                    "name": "minecraft:poisonous_potato",
                    "functions": [
                        {
                        "function": "minecraft:set_components",
                        "components": {
                            "minecraft:item_name": {"translate":f"item.{data_array[i+csv_offset][1]}.{data_array[i+csv_offset][2]}","fallback":f"{data_array[i+csv_offset][3]}"},
                            "minecraft:item_model": f"{data_array[i+csv_offset][1]}:{data_array[i+csv_offset][2]}",
                            "minecraft:food": {
                            "nutrition": to_int(data_array[i+csv_offset][5]),
                            "saturation": to_float(data_array[i+csv_offset][6])
                            },
                            "minecraft:consumable": {},
                            "minecraft:custom_data": {f"{data_array[i+csv_offset][1]}":{"ingredient":{"type":f"{data_array[i+csv_offset][2]}"}},"smithed":{"ignore":{"functionality":True,"crafting":True}}},
                            "minecraft:lore": [{"translate":f"{data_array[i+csv_offset][1]}.tooltip","font":f"{data_array[i+csv_offset][1]}:tooltip","color":"white","italic":False}]
                        }
                        }
                    ]
                    }
                ]
                }
            ]
        }
    else:
        loot = {
            "pools": [
                {
                "rolls": 1,
                "entries": [
                    {
                    "type": "minecraft:item",
                    "name": "minecraft:splash_potion",
                    "functions": [
                        {
                        "function": "minecraft:set_components",
                        "components": {
                            "minecraft:max_stack_size": 1,
                            "minecraft:item_name": {"translate":f"item.{data_array[i+csv_offset][1]}.{data_array[i+csv_offset][2]}","fallback":f"{data_array[i+csv_offset][3]}"},
                            "minecraft:item_model": f"{data_array[i+csv_offset][1]}:{data_array[i+csv_offset][2]}",
                            "minecraft:potion_contents": {
                            "custom_color": to_int(data_array[i+csv_offset][15]),
                            "custom_name": f"{data_array[i+csv_offset][2]}"
                            },
                            "minecraft:tooltip_display": {
                            "hidden_components": [
                                "minecraft:potion_contents"
                            ]
                            },
                            "minecraft:lore": [{"translate":"item.cnk.calendar.format", "with": ["0", "0"],"color":"blue","italic":False},{"translate":f"{data_array[i+csv_offset][1]}.tooltip","font":f"{data_array[i+csv_offset][1]}:tooltip","color":"white","italic":False}],
                            "minecraft:custom_data": {f"{data_array[i+csv_offset][1]}":{"ingredient":{"type":f"{data_array[i+csv_offset][2]}"}},"cnk":{"wine":{"time":0,"color":to_int(data_array[i+csv_offset][15])}},"smithed":{"ignore":{"functionality":True,"crafting":True}}}
                        }
                        }
                    ]
                    }
                ]
                }
            ]
        }

    write_to_file(f"data/{data_array[i+csv_offset][1]}/loot_table/{data_array[i+csv_offset][7]}",f"{data_array[i+csv_offset][2]}.json",loot,i,"w") 

    # recipe check
    if data_array[i+csv_offset][9] in worklstation_list:
        if data_array[i+csv_offset][9] != "distiller":
            # cookbook
            # grant
            grant = [f"function cnk:cookbook/database/set/main {{flag:\"item.{data_array[i+csv_offset][1]}.{data_array[i+csv_offset][2]}\"}}\n",
                    f"execute unless score $set_success cnk.dummy matches 1 run return run advancement revoke @s only {data_array[i+csv_offset][1]}:cookbook/{data_array[i+csv_offset][2]}/item\n",
                    f"advancement grant @s[tag=!cnk.cookbook_unlock,tag=!cnk.no_toasts] only {data_array[i+csv_offset][1]}:cookbook/{data_array[i+csv_offset][2]}/toast\n"]
            write_to_file(f"data/{data_array[i+csv_offset][1]}/function/cookbook/grant",f"{data_array[i+csv_offset][2]}.mcfunction",grant,i,"w")
            
            # page
            ingredient_cols = [data_array[i+csv_offset][10], data_array[i+csv_offset][11], data_array[i+csv_offset][12], 
                            data_array[i+csv_offset][13], data_array[i+csv_offset][14]]

            ingredient_lines = []
            for ingredient in ingredient_cols:
                if ingredient:  # skip empty
                    namespace = ingredient.split(".")[0]  # extract namespace from ingredient
                    font = "cnk.book:icons" if namespace in ("cnk", "minecraft") else f"{namespace}:icons"
                    ingredient_lines.append(f"    {{key:\"item.{ingredient}\", font:\"{font}\"}}, \\\n")

            if ingredient_lines:
                ingredient_lines[-1] = ingredient_lines[-1].replace("},", "}", 1) # remove trailing comma

            page = [f"execute store result storage cnk:temp register.page_number int 1 run scoreboard players get $global_cookbook_page cnk.dummy\n",
                    "\n",
                    f"data modify storage cnk:temp register.tool set value \"{data_array[i+csv_offset][1]}.{data_array[i+csv_offset][9]}\"\n",
                    f"data modify storage cnk:temp register.page_name set value \"item.{data_array[i+csv_offset][1]}.{data_array[i+csv_offset][2]}\"\n",
                    f"data modify storage cnk:temp register.recipe_icon_font set value \"{data_array[i+csv_offset][1]}:icons\"\n",
                    "\n",
                    "data modify storage cnk:temp register.ingredients set value [ \\\n",
                    *ingredient_lines,
                    "]\n",
                    "\n",
                    f"data modify storage cnk:temp register.source set value {{key:\"{data_array[i+csv_offset][1]}.source\", font:\"{data_array[i+csv_offset][1]}:icons\"}}\n",
                    "\n",
                    "function cnk:cookbook/pages/register\n"]

            group = data_array[i+csv_offset][8]
            if group in cookbook_groups:
                idx = cookbook_groups.index(group)
                cookbook_pages[idx].append(f"{data_array[i+csv_offset][1]}:cookbook/pages/{data_array[i+csv_offset][2]}")
            write_to_file(f"data/{data_array[i+csv_offset][1]}/function/cookbook/page",f"{data_array[i+csv_offset][2]}.mcfunction",page,i,"w")

            
            # recipe
            if data_array[i+csv_offset][9] == "cooking_pot":

                recipe_lines = ["execute \\\n"]
                result_lines = []

                for ingredient in ingredient_cols:
                    if ingredient:
                        namespace = ingredient.split(".")[0]
                        item = ingredient.split(".")[1]
                        
                        if namespace == "minecraft":
                            recipe_lines.append(f"        if data storage cnk:temp cooking_pot.Items[{{id:\"minecraft:{item}\"}}] \\\n")
                            result_lines.append(f"data modify storage cnk:temp cooking_pot.slot set from storage cnk:temp cooking_pot.Items[{{id:\"minecraft:{item}\"}}].Slot\n")
                        else:
                            recipe_lines.append(f"        if data storage cnk:temp cooking_pot.Items[{{components:{{\"minecraft:custom_data\":{{{namespace}:{{ingredient:{{type:\"{item}\"}}}}}}}}}}] \\\n")
                            result_lines.append(f"data modify storage cnk:temp cooking_pot.slot set from storage cnk:temp cooking_pot.Items[{{components:{{\"minecraft:custom_data\":{{{namespace}:{{ingredient:{{type:\"{item}\"}}}}}}}}}}].Slot\n")
                        
                        result_lines.append(f"function cnk:recipes/remove with storage cnk:temp cooking_pot\n")
                        result_lines.append("\n")

                recipe_lines.append(f"        if function cnk:cooking_pot/crafting/lock \\\n")
                recipe_lines.append(f"        run return run function {data_array[i+csv_offset][1]}:cooking_pot/recipes/{data_array[i+csv_offset][2]}\n")
                result_lines.append(f"# spawn the result\n")
                result_lines.append(f"loot spawn ~ ~0.25 ~ loot {data_array[i+csv_offset][1]}:food/{data_array[i+csv_offset][2]}\n")
                result_lines.append("\n")
                result_lines.append("# MUST be called, handles animations/sounds and reset of data\n")
                result_lines.append("function cnk:cooking_pot/effects/finish_cooking\n")

                write_to_file(f"data/{data_array[i+csv_offset][1]}/function/cooking_pot",f"{len([x for x in ingredient_cols if x])}.mcfunction",recipe_lines,i,"a")
                write_to_file(f"data/{data_array[i+csv_offset][1]}/function/cooking_pot/recipes",f"{data_array[i+csv_offset][2]}.mcfunction",result_lines,i,"w")


            elif data_array[i+csv_offset][9] == "cutting_board":
                namespace = data_array[i+csv_offset][10].split(".")[0]
                item = data_array[i+csv_offset][10].split(".")[1]

                if namespace == "minecraft":
                    recipe_lines = [f"execute if data storage cnk:temp cutting_board.item{{id:\"minecraft:{item}\"}} run return run function {data_array[i+csv_offset][1]}:cutting_board/recipes/{data_array[i+csv_offset][2]}\n"]
                else:
                    recipe_lines = [f"execute if data storage cnk:temp cutting_board.item{{components:{{\"minecraft:custom_data\":{{\"{namespace}\":{{\"ingredient\":{{\"type\":\"{item}\"}}}}}}}}}} run return run function {data_array[i+csv_offset][1]}:cutting_board/recipes/{data_array[i+csv_offset][2]}\n"]

                result_lines = ["# this function is called once the player uses the knife on the cutting board! nice and simple, just spawns the output item, and handles tidy up\n",
                                f"loot spawn ~ ~-0.3 ~ loot {data_array[i+csv_offset][1]}:{data_array[i+csv_offset][7]}/{data_array[i+csv_offset][2]}\n",
                                "\n",
                                "# this function MUST be called, tidies up the item and triggers sound and durability change\n",
                                "function cnk:cutting_board/cut/finish\n"]

                write_to_file(f"data/{data_array[i+csv_offset][1]}/function/cutting_board","recipes.mcfunction",recipe_lines,i,"a")
                write_to_file(f"data/{data_array[i+csv_offset][1]}/function/cutting_board/recipes",f"{data_array[i+csv_offset][2]}.mcfunction",result_lines,i,"w")

            elif data_array[i+csv_offset][9] == "mixing_bowl":
                recipe_lines = [f"execute if score $mixing_bowl_item_count cnk.dummy matches {len([x for x in ingredient_cols if x])} \\\n"]
                result_lines = [f"loot spawn ~ ~0.3 ~ loot {data_array[i+csv_offset][1]}:{data_array[i+csv_offset][7]}/{data_array[i+csv_offset][2]}\n",
                                "\n",
                                "function cnk:mixing_bowl/mix/clean_up\n"]

                for ingredient in ingredient_cols:
                    if ingredient:
                        namespace = ingredient.split(".")[0]
                        item = ingredient.split(".")[1]
                        
                        if namespace == "minecraft":
                            recipe_lines.append(f"        if data storage cnk:temp mixing_bowl.Items[{{id:\"minecraft:{item}\"}}] \\\n")
                        else:
                            recipe_lines.append(f"        if data storage cnk:temp mixing_bowl.Items[{{components:{{\"minecraft:custom_data\":{{{namespace}:{{ingredient:{{type:\"{item}\"}}}}}}}}}}] \\\n")   

                recipe_lines.append(f"        if function cnk:mixing_bowl/mix/lock \\\n")
                recipe_lines.append(f"        run return run data modify entity @s item.components.\"minecraft:custom_data\".cnk.mix_callback set value \"{data_array[i+csv_offset][1]}:mixing_bowl/recipes/{data_array[i+csv_offset][2]}\"\n")

                write_to_file(f"data/{data_array[i+csv_offset][1]}/function/mixing_bowl","recipes.mcfunction",recipe_lines,i,"a")
                write_to_file(f"data/{data_array[i+csv_offset][1]}/function/mixing_bowl/recipes",f"{data_array[i+csv_offset][2]}.mcfunction",result_lines,i,"w")

                
            else:
                recipe_lines = [f"execute if score ${data_array[i+csv_offset][9]}_item_count cnk.dummy matches {len([x for x in ingredient_cols if x])} \\\n"]
                result_lines = [f"loot spawn ~ ~0.25 ~ loot {data_array[i+csv_offset][1]}:{data_array[i+csv_offset][7]}/{data_array[i+csv_offset][2]}\n",
                                "\n",
                                f"function {data_array[i+csv_offset][1]}:{data_array[i+csv_offset][9]}/{data_array[i+csv_offset][17]}/clean_up\n"]

                for ingredient in ingredient_cols:
                    if ingredient:
                        namespace = ingredient.split(".")[0]
                        item = ingredient.split(".")[1]
                        
                        if namespace == "minecraft":
                            recipe_lines.append(f"        if data storage cnk:temp {data_array[i+csv_offset][9]}.Items[{{id:\"minecraft:{item}\"}}] \\\n")
                        else:
                            recipe_lines.append(f"        if data storage cnk:temp {data_array[i+csv_offset][9]}.Items[{{components:{{\"minecraft:custom_data\":{{{namespace}:{{ingredient:{{type:\"{item}\"}}}}}}}}}}] \\\n")   

                recipe_lines.append(f"        if function {data_array[i+csv_offset][1]}:{data_array[i+csv_offset][9]}/{data_array[i+csv_offset][17]}/lock \\\n")
                recipe_lines.append(f"        run return run data modify entity @s item.components.\"minecraft:custom_data\".{data_array[i+csv_offset][1]}.{data_array[i+csv_offset][17]}_callback set value \"{data_array[i+csv_offset][1]}:recipes/{data_array[i+csv_offset][9]}/{data_array[i+csv_offset][2]}\"\n")


                write_to_file(f"data/{data_array[i+csv_offset][1]}/function/{data_array[i+csv_offset][9]}/{data_array[i+csv_offset][17]}","recipes.mcfunction",recipe_lines,i,"a")
                write_to_file(f"data/{data_array[i+csv_offset][1]}/function/recipes/{data_array[i+csv_offset][9]}",f"{data_array[i+csv_offset][2]}.mcfunction",result_lines,i,"w")
        else:
            # distiller
            
            # page
            ingredient_cols = [data_array[i+csv_offset][10], data_array[i+csv_offset][11], data_array[i+csv_offset][12], 
                            data_array[i+csv_offset][13], data_array[i+csv_offset][14]]

            ingredient_lines = []
            for ingredient in ingredient_cols:
                if ingredient:  # skip empty
                    namespace = ingredient.split(".")[0]  # extract namespace from ingredient
                    font = "cnk.book:icons" if namespace in ("cnk", "minecraft") else f"{namespace}:icons"
                    ingredient_lines.append(f"    {{key:\"item.{ingredient}\", font:\"{font}\"}}, \\\n")

            if ingredient_lines:
                ingredient_lines[-1] = ingredient_lines[-1].replace("},", "}", 1) # remove trailing comma

            page = ["# sets the page number from the current global, MUST be present\n",
                    "execute store result storage cnk:temp register.page_number int 1 run scoreboard players get $global_distiller_book_page cnk.dummy\n"
                    "\n",
                    "# sets the page name\n",
                    f"data modify storage cnk:temp register.page_name set value \"item.{data_array[i+csv_offset][1]}.{data_array[i+csv_offset][2]}\"\n",
                    "\n",
                    "# sets the ingredients\n",
                    "data modify storage cnk:temp register.ingredients set value [ \\\n",
                    *ingredient_lines,
                    "]\n",
                    "\n",
                    f"data modify storage cnk:temp register.source set value {{key:\"{data_array[i+csv_offset][1]}.source\", font:\"{data_array[i+csv_offset][1]}:icons\"}}\n",
                    "\n",
                    "# register the page\n",
                    "function cnk:cookbook/pages/register\n"]
            distiller_pages.append(f"{data_array[i+csv_offset][1]}:distiller_book/pages/{data_array[i+csv_offset][2]}")
            write_to_file(f"data/{data_array[i+csv_offset][1]}/function/distiller_book/pages",f"{data_array[i+csv_offset][2]}.mcfunction",page,i,"w")

            # liquid_check
            liquid_check = ["# checks the basin to see if the liquid matches the one about to be crafted, or if it is empty\n",
                            "# you need to make one of these for every new liquid you add\n",
                            f"execute if data storage cnk:temp distiller.basin{{liquid:\"{data_array[i+csv_offset][2]}\"}} run return 1\n",
                            "execute if data storage cnk:temp distiller.basin{liquid:\"\"} run return 1\n",
                            "return fail"]
            write_to_file(f"data/{data_array[i+csv_offset][1]}/function/distiller/liquid_check",f"{data_array[i+csv_offset][2]}.mcfunction",liquid_check,i,"w")
            
            # drink
            drink = [f"execute if entity @s[predicate=cnk:inventory_full] run return run loot spawn ~ ~ ~ loot {data_array[i+csv_offset][1]}:{data_array[i+csv_offset][7]}/{data_array[i+csv_offset][2]}\n",
                     f"loot give @s loot {data_array[i+csv_offset][1]}:{data_array[i+csv_offset][7]}/{data_array[i+csv_offset][2]}"]
            write_to_file(f"data/{data_array[i+csv_offset][1]}/function/distiller/drinks/{data_array[i+csv_offset][2]}","main.mcfunction",drink,i,"w")
            
            # recipes
            recipes = ["# woah! more compliciated!\n",
                        "\n"
                            "# these remove the items from the distiller, just like the cooking pot. once again some helper functions exist for generic items\n",
                            "function cnk:recipes/distiller/generic/water\n",
                            "\n"]
            
            for ingredient in ingredient_cols:
                if ingredient:
                    namespace = ingredient.split(".")[0]
                    item = ingredient.split(".")[1]
                    
                    if namespace == "minecraft":
                        recipes.append(f"data modify storage cnk:temp {data_array[i+csv_offset][9]}.slot set from storage cnk:temp {data_array[i+csv_offset][9]}.Items[{{id:\"minecraft:{item}\"}}] \n")
                        recipes.append(f"function cnk:recipes/remove with storage cnk:temp {data_array[i+csv_offset][9]}\n\n")
                    else:
                        recipes.append(f"data modify storage cnk:temp {data_array[i+csv_offset][9]}.slot set from storage cnk:temp {data_array[i+csv_offset][9]}.Items[{{components:{{\"minecraft:custom_data\":{{{namespace}:{{ingredient:{{type:\"{item}\"}}}}}}}}}}] \n")
                        recipes.append(f"function cnk:recipes/remove with storage cnk:temp {data_array[i+csv_offset][9]}\n\n")

            recipes.append("# sets the colour of the liquid to be output, this is the colour that will also appear in the basin\n")
            recipes.append("# the minecraft wiki has a useful tool for converting colours to decimal format\n")
            recipes.append("# https://minecraft.wiki/w/Data_component_format#custom_model_data\n")
            recipes.append(f"data modify storage cnk:temp {data_array[i+csv_offset][9]}.color set value {data_array[i+csv_offset][15]}\n")
            recipes.append("\n")
            recipes.append("# sets the callback function that will be called when a player uses a glass bottle on the basin with liquid in it\n")
            recipes.append(f"data modify storage cnk:temp distiller.callback set value \"{data_array[i+csv_offset][1]}:{data_array[i+csv_offset][9]}/drinks/{data_array[i+csv_offset][2]}/main\"\n")
            recipes.append("\n")
            recipes.append("# sets the liquid type, used in the liquid_check functions so must match\n")
            recipes.append(f"data modify storage cnk:temp distiller.liquid set value \"{data_array[i+csv_offset][2]}\"\n")
            recipes.append("\n")
            recipes.append("# MUST be called, handles animations and setting the data on the basin\n")
            recipes.append("function cnk:distiller/crafting/finish_distilling")

            write_to_file(f"data/{data_array[i+csv_offset][1]}/function/distiller/recipes",f"{data_array[i+csv_offset][2]}.mcfunction",recipes,i,"w")

            # recipe.mcfunction

            #recipe_lines = ["# unlike the cooking pot, the distiller does not split up its recipe files based on unique item quantities, there's just way less recipe so it's not necessary\n",                            "# when added to the distiller tag, recipes in this file will be used for distilling:\n",                            "# - cnk:tags/function/addons/distiller\n",                            "\n",                            "# setup is very similar to the cooking pot, with the exception that the quantity of items must be checked first\n",                            "# cnk comes with 2 lock functions, which basically just handle 2 different crafting times:\n",                            "# - cnk:distiller/crafting/short_lock - 15 second crafting time\n",                            "# - cnk:distiller/crafting/lock - 20 minute crafting time (1 minecraft day, for wines)\n",                            "# you can define new lock functions if you need different crafting times, just take a look at those functions to see their layout\n",                            "\n",                            "# both the cooking pot and distiller identify unique items by the presence of custom data\n",                            "# if the custom data component is present, it will no longer be counted as its base vanilla item and its custom data will instead be used as a unique identifier\n",                            "# you don't need to worry about this too much, beyond just making sure that your custom items have some amount of custom data that makes them unique!\n",                            "\n",                            "# the cnk:temp distiller.Items storage contains the contents of the distiller, so you can check for any sort of data!\n",                            "\n",                            "# you MUST define a new liquid_check function for any new liquids, these basically check the basin the distiller will output into, to make sure its empty or has the same liquid in it\n\n"]

            recipe_lines = ["execute \\\n",
                            f"        if score $unique_items cnk.dummy matches {len([x for x in ingredient_cols if x])} \\\n"]

            for ingredient in ingredient_cols:
                if ingredient:
                    namespace = ingredient.split(".")[0]
                    item = ingredient.split(".")[1]
                    
                    if namespace == "minecraft":
                        recipe_lines.append(f"        if data storage cnk:temp distiller.Items[{{id:\"minecraft:{item}\"}}] \\\n")
                    else:
                        recipe_lines.append(f"        if data storage cnk:temp distiller.Items[{{components:{{\"minecraft:custom_data\":{{{namespace}:{{ingredient:{{type:\"{item}\"}}}}}}}}}}] \\\n")   

            # split distill_time
            s = data_array[i+csv_offset][18]
            num_str = s.rstrip('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
            suffix = s[len(num_str):]
            value = int(num_str)
            if suffix == "d":
                time = value * 1200
            elif suffix == "m":
                time = value * 60
            else:
                time = value

            if time == 1200:
                recipe_lines.append(f"        if function cnk:distiller/crafting/lock \\\n")
            elif time == 15:
                recipe_lines.append(f"        if function cnk:distiller/crafting/short_lock \\\n")
            else:
                recipe_lines.append(f"        if function {data_array[i+csv_offset][1]}:{data_array[i+csv_offset][9]}/crafting/lock_{time}s \\\n")
                lock = [f"scoreboard players set $distill_time cnk.dummy {20 * time}\n",
                        "execute if function cnk:distiller/crafting/process run return 1\n",
                        "return fail"]
                write_to_file(f"data/{data_array[i+csv_offset][1]}/function/distiller/crafting",f"lock_{time}s.mcfunction",lock,i,"w")
            recipe_lines.append(f"        run return run function {data_array[i+csv_offset][1]}:distiller/recipes/{data_array[i+csv_offset][2]}\n")


            write_to_file(f"data/{data_array[i+csv_offset][1]}/function/distiller","recipes.mcfunction",recipe_lines,i,"a")

# cookbook and distiller pages
#cookbook
for group, pages in zip(cookbook_groups, cookbook_pages):
    pages_data = {"values": pages}
    write_to_file("data/cnk/tags/function/cookbook", f"{group}.json", pages_data, 0, "w")

#distiller
pages_data = {"values": distiller_pages}
write_to_file("data/cnk/tags/function/distiller_book", "pages.json", pages_data, 0, "w")

for namespace, entries in lang_entries.items():
    write_to_file(f"assets/{namespace}/lang", "en_us.json", entries, 0, "w")

for namespace, providers in icon_entries.items():
    write_to_file(f"assets/{namespace}/font", "icons.json", {"providers": providers}, 0, "w")