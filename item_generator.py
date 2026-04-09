import csv
import json
from pathlib import Path

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

# read csv
with open('data.csv', newline='') as f:
    reader = csv.reader(f)
    # Convert reader object directly to a list
    data_array = list(reader)


# find workstations
worklstation_list = list(set(data_array[i+10][9] for i in range(len(data_array)-10)))
worklstation_list = [x for x in worklstation_list if x]
#print(worklstation_list)



for i in range(len(data_array)-10):
    #print(data_array[i+10])


    # model files
    model = {
        "parent": "minecraft:item/generated",
        "textures": {
            "layer0": f"{data_array[i+10][1]}:item/{data_array[i+10][2]}"
        }
    }

    directory = Path(f"assets/{data_array[i+10][1]}/models/item")
    file_path = directory / f"{data_array[i+10][2]}.json"
    directory.mkdir(parents=True, exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(model, f, indent=4)
    

    # item files
    item = {
        "model": {
            "type": "minecraft:model",
            "model": f"{data_array[i+10][1]}:item/{data_array[i+10][2]}"
        }
    }

    directory = Path(f"assets/{data_array[i+10][1]}/items")
    file_path = directory / f"{data_array[i+10][2]}.json"
    directory.mkdir(parents=True, exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(item, f, indent=4)
    

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
                    "minecraft:custom_data": {f"{data_array[i+10][1]}":{"ingredient":{"type":f"{data_array[i+10][2]}"}}}
                    }
                }
                ]
            }
            }
        },
        "rewards": {
            "function": f"{data_array[i+10][1]}:cookbook/grant/{data_array[i+10][2]}"
        }
    }

    toast = {
        "parent": "cnk:cookbook/toasts",
        "display": {
            "title": [{"translate":"book.cnk.toast.background","font":"cnk.book:advancement"},{"translate":f"book.cnk.toast.unlock.{data_array[i+10][4]}","font":"cnk.book:advancement_text","color":"#7b613a"}],
            "icon": {
            "id": "minecraft:poisonous_potato",
            "components": {"minecraft:item_model": f"{data_array[i+10][1]}:{data_array[i+10][2]}"}
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

    directory = Path(f"data/{data_array[i+10][1]}/advancement/cookbook/{data_array[i+10][2]}")
    file_path = directory / "item.json"
    directory.mkdir(parents=True, exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(item, f, indent=4)

    file_path = directory / "toast.json"
    directory.mkdir(parents=True, exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(toast, f, indent=4)
    

    # loot tables
    if data_array[i+10][16] != "TRUE":
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
                            "minecraft:item_name": {"translate":f"item.{data_array[i+10][1]}.{data_array[i+10][2]}","fallback":f"{data_array[i+10][3]}"},
                            "minecraft:item_model": f"{data_array[i+10][1]}:{data_array[i+10][2]}",
                            "minecraft:food": {
                            "nutrition": to_int(data_array[i+10][5]),
                            "saturation": to_float(data_array[i+10][6])
                            },
                            "minecraft:consumable": {},
                            "minecraft:custom_data": {f"{data_array[i+10][1]}":{"ingredient":{"type":f"{data_array[i+10][2]}"}},"smithed":{"ignore":{"functionality":True,"crafting":True}}},
                            "minecraft:lore": [{"translate":f"{data_array[i+10][1]}.tooltip","font":f"{data_array[i+10][1]}:tooltip","color":"white","italic":False}]
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
                            "minecraft:item_name": {"translate":f"item.{data_array[i+10][1]}.{data_array[i+10][2]}","fallback":f"{data_array[i+10][3]}"},
                            "minecraft:item_model": f"{data_array[i+10][1]}:{data_array[i+10][2]}",
                            "minecraft:potion_contents": {
                            "custom_color": to_int(data_array[i+10][15]),
                            "custom_name": f"{data_array[i+10][2]}"
                            },
                            "minecraft:tooltip_display": {
                            "hidden_components": [
                                "minecraft:potion_contents"
                            ]
                            },
                            "minecraft:lore": [{"translate":"item.cnk.calendar.format", "with": ["0", "0"],"color":"blue","italic":False},{"translate":f"{data_array[i+10][1]}.tooltip","font":f"{data_array[i+10][1]}:tooltip","color":"white","italic":False}],
                            "minecraft:custom_data": {f"{data_array[i+10][1]}":{"ingredient":{"type":f"{data_array[i+10][2]}"}},"cnk":{"wine":{"time":0,"color":to_int(data_array[i+10][15])}},"smithed":{"ignore":{"functionality":True,"crafting":True}}}
                        }
                        }
                    ]
                    }
                ]
                }
            ]
        }

    directory = Path(f"data/{data_array[i+10][1]}/loot_table/{data_array[i+10][7]}")
    file_path = directory / f"{data_array[i+10][2]}.json"
    directory.mkdir(parents=True, exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(loot, f, indent=4)
    

    # recipe check
    if data_array[i+10][9] in worklstation_list:
        if data_array[i+10][9] != "distiller":
            # cookbook
            # grant
            grant = [f"function cnk:cookbook/database/set/main {{flag:\"item.{data_array[i+10][1]}.{data_array[i+10][2]}\"}}\n",
                    f"execute unless score $set_success cnk.dummy matches 1 run return run advancement revoke @s only {data_array[i+10][1]}:cookbook/{data_array[i+10][2]}/item\n",
                    f"advancement grant @s[tag=!cnk.cookbook_unlock,tag=!cnk.no_toasts] only {data_array[i+10][1]}:cookbook/{data_array[i+10][2]}/toast\n"]

            directory = Path(f"data/{data_array[i+10][1]}/function/cookbook/grant")
            file_path = directory / f"{data_array[i+10][2]}.mcfunction"
            directory.mkdir(parents=True, exist_ok=True)
            with open(file_path, "w", encoding="utf-8") as f:
                f.writelines(grant)
            
            # page
            ingredient_cols = [data_array[i+10][10], data_array[i+10][11], data_array[i+10][12], 
                            data_array[i+10][13], data_array[i+10][14]]

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
                    f"data modify storage cnk:temp register.tool set value \"{data_array[i+10][1]}.{data_array[i+10][9]}\"\n",
                    f"data modify storage cnk:temp register.page_name set value \"item.{data_array[i+10][1]}.{data_array[i+10][2]}\"\n",
                    f"data modify storage cnk:temp register.recipe_icon_font set value \"{data_array[i+10][1]}:icons\"\n",
                    "\n",
                    "data modify storage cnk:temp register.ingredients set value [ \\\n",
                    *ingredient_lines,
                    "]\n",
                    "\n",
                    f"data modify storage cnk:temp register.source set value {{key:\"{data_array[i+10][1]}.source\", font:\"{data_array[i+10][1]}:icons\"}}\n",
                    "\n",
                    "function cnk:cookbook/pages/register\n"]

            directory = Path(f"data/{data_array[i+10][1]}/function/cookbook/grant")
            file_path = directory / f"{data_array[i+10][2]}.mcfunction"
            directory.mkdir(parents=True, exist_ok=True)
            with open(file_path, "w", encoding="utf-8") as f:
                f.writelines(page)
            
            # recipe
            if data_array[i+10][9] == "cooking_pot":

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
                recipe_lines.append(f"        run return run function {data_array[i+10][1]}:cooking_pot/recipes/{data_array[i+10][2]}\n")
                result_lines.append(f"# spawn the result\n")
                result_lines.append(f"loot spawn ~ ~0.25 ~ loot {data_array[i+10][1]}:food/{data_array[i+10][2]}\n")
                result_lines.append("\n")
                result_lines.append("# MUST be called, handles animations/sounds and reset of data\n")
                result_lines.append("function cnk:cooking_pot/effects/finish_cooking\n")

                directory = Path(f"data/{data_array[i+10][1]}/function/cooking_pot")
                file_path = directory / f"{len([x for x in ingredient_cols if x])}.mcfunction"
                directory.mkdir(parents=True, exist_ok=True)
                with open(file_path, "a", encoding="utf-8") as f:
                    f.writelines(recipe_lines)

                directory = Path(f"data/{data_array[i+10][1]}/function/cooking_pot/recipes")
                file_path = directory / f"{data_array[i+10][2]}.mcfunction"
                directory.mkdir(parents=True, exist_ok=True)
                with open(file_path, "w", encoding="utf-8") as f:
                    f.writelines(result_lines)

            elif data_array[i+10][9] == "cutting_board":
                namespace = data_array[i+10][10].split(".")[0]
                item = data_array[i+10][10].split(".")[1]

                if namespace == "minecraft":
                    recipe_lines = [f"execute if data storage cnk:temp cutting_board.item{{id:\"minecraft:{item}\"}} run return run function {data_array[i+10][1]}:cutting_board/recipes/{data_array[i+10][2]}\n"]
                else:
                    recipe_lines = [f"execute if data storage cnk:temp cutting_board.item{{components:{{\"minecraft:custom_data\":{{\"{namespace}\":{{\"ingredient\":{{\"type\":\"{item}\"}}}}}}}}}} run return run function {data_array[i+10][1]}:cutting_board/recipes/{data_array[i+10][2]}\n"]

                result_lines = ["# this function is called once the player uses the knife on the cutting board! nice and simple, just spawns the output item, and handles tidy up\n",
                                f"loot spawn ~ ~-0.3 ~ loot {data_array[i+10][1]}:{data_array[i+10][7]}/{data_array[i+10][2]}\n",
                                "\n",
                                "# this function MUST be called, tidies up the item and triggers sound and durability change\n",
                                "function cnk:cutting_board/cut/finish\n"]

                directory = Path(f"data/{data_array[i+10][1]}/function/cutting_board")
                file_path = directory / "recipes.mcfunction"
                directory.mkdir(parents=True, exist_ok=True)
                with open(file_path, "a", encoding="utf-8") as f:
                    f.writelines(recipe_lines)
                
                directory = Path(f"data/{data_array[i+10][1]}/function/cutting_board/recipes")
                file_path = directory / f"{data_array[i+10][2]}.mcfunction"
                directory.mkdir(parents=True, exist_ok=True)
                with open(file_path, "w", encoding="utf-8") as f:
                    f.writelines(result_lines)

            elif data_array[i+10][9] == "mixing_bowl":
                recipe_lines = [f"execute if score $mixing_bowl_item_count cnk.dummy matches {len([x for x in ingredient_cols if x])} \\\n"]
                result_lines = [f"loot spawn ~ ~0.3 ~ loot {data_array[i+10][1]}:{data_array[i+10][7]}/{data_array[i+10][2]}\n",
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
                recipe_lines.append(f"        run return run data modify entity @s item.components.\"minecraft:custom_data\".cnk.mix_callback set value \"{data_array[i+10][1]}:mixing_bowl/recipes/{data_array[i+10][2]}\"\n")

                directory = Path(f"data/{data_array[i+10][1]}/function/mixing_bowl")
                file_path = directory / "recipes.mcfunction"
                directory.mkdir(parents=True, exist_ok=True)
                with open(file_path, "a", encoding="utf-8") as f:
                    f.writelines(recipe_lines)
                
                directory = Path(f"data/{data_array[i+10][1]}/function/mixing_bowl/recipes")
                file_path = directory / f"{data_array[i+10][2]}.mcfunction"
                directory.mkdir(parents=True, exist_ok=True)
                with open(file_path, "w", encoding="utf-8") as f:
                    f.writelines(result_lines)
                
            else:
                recipe_lines = [f"execute if score ${data_array[i+10][9]}_item_count cnk.dummy matches {len([x for x in ingredient_cols if x])} \\\n"]
                result_lines = [f"loot spawn ~ ~0.25 ~ loot {data_array[i+10][1]}:{data_array[i+10][7]}/{data_array[i+10][2]}\n",
                                "\n",
                                f"function {data_array[i+10][1]}:{data_array[i+10][9]}/{data_array[i+10][17]}/clean_up\n"]

                for ingredient in ingredient_cols:
                    if ingredient:
                        namespace = ingredient.split(".")[0]
                        item = ingredient.split(".")[1]
                        
                        if namespace == "minecraft":
                            recipe_lines.append(f"        if data storage cnk:temp {data_array[i+10][9]}.Items[{{id:\"minecraft:{item}\"}}] \\\n")
                        else:
                            recipe_lines.append(f"        if data storage cnk:temp {data_array[i+10][9]}.Items[{{components:{{\"minecraft:custom_data\":{{{namespace}:{{ingredient:{{type:\"{item}\"}}}}}}}}}}] \\\n")   

                recipe_lines.append(f"        if function {data_array[i+10][1]}:{data_array[i+10][9]}/{data_array[i+10][17]}/lock \\\n")
                recipe_lines.append(f"        run return run data modify entity @s item.components.\"minecraft:custom_data\".{data_array[i+10][1]}.{data_array[i+10][17]}_callback set value \"{data_array[i+10][1]}:recipes/{data_array[i+10][9]}/{data_array[i+10][2]}\"\n")
                
                directory = Path(f"data/{data_array[i+10][1]}/function/{data_array[i+10][9]}/{data_array[i+10][17]}")
                file_path = directory / "recipes.mcfunction"
                directory.mkdir(parents=True, exist_ok=True)
                with open(file_path, "a", encoding="utf-8") as f:
                    f.writelines(recipe_lines)
                
                directory = Path(f"data/{data_array[i+10][1]}/function/recipes/{data_array[i+10][9]}")
                file_path = directory / f"{data_array[i+10][2]}.mcfunction"
                directory.mkdir(parents=True, exist_ok=True)
                with open(file_path, "w", encoding="utf-8") as f:
                    f.writelines(result_lines)
        else:
            # distiller
            
            # page
            ingredient_cols = [data_array[i+10][10], data_array[i+10][11], data_array[i+10][12], 
                            data_array[i+10][13], data_array[i+10][14]]

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
                    f"data modify storage cnk:temp register.page_name set value \"item.{data_array[i+10][1]}.{data_array[i+10][2]}\"\n",
                    "\n",
                    "# sets the ingredients\n",
                    "data modify storage cnk:temp register.ingredients set value [ \\\n",
                    *ingredient_lines,
                    "]\n",
                    "\n",
                    f"data modify storage cnk:temp register.source set value {{key:\"{data_array[i+10][1]}.source\", font:\"{data_array[i+10][1]}:icons\"}}\n",
                    "\n",
                    "# register the page\n",
                    "function cnk:cookbook/pages/register\n"]

            directory = Path(f"data/{data_array[i+10][1]}/function/distiller_book/pages")
            file_path = directory / f"{data_array[i+10][2]}.mcfunction"
            directory.mkdir(parents=True, exist_ok=True)
            with open(file_path, "w", encoding="utf-8") as f:
                f.writelines(page)

            # liquid_check
            liquid_check = ["# checks the basin to see if the liquid matches the one about to be crafted, or if it is empty\n",
                            "# you need to make one of these for every new liquid you add\n",
                            f"execute if data storage cnk:temp distiller.basin{{liquid:\"{data_array[i+10][2]}\"}} run return 1\n",
                            "execute if data storage cnk:temp distiller.basin{liquid:\"\"} run return 1\n",
                            "return fail"]
            
            directory = Path(f"data/{data_array[i+10][1]}/function/distiller/liquid_check")
            file_path = directory / f"{data_array[i+10][2]}.mcfunction"
            directory.mkdir(parents=True, exist_ok=True)
            with open(file_path, "w", encoding="utf-8") as f:
                f.writelines(liquid_check)
            
            # drink
            drink = [f"execute if entity @s[predicate=cnk:inventory_full] run return run loot spawn ~ ~ ~ loot {data_array[i+10][1]}:{data_array[i+10][7]}/{data_array[i+10][2]}\n",
                     f"loot give @s loot {data_array[i+10][1]}:{data_array[i+10][7]}/{data_array[i+10][2]}"]
            
            directory = Path(f"data/{data_array[i+10][1]}/function/distiller/drinks/{data_array[i+10][2]}")
            file_path = directory / "main.mcfunction"
            directory.mkdir(parents=True, exist_ok=True)
            with open(file_path, "w", encoding="utf-8") as f:
                f.writelines(drink)
            
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
                        recipes.append(f"data modify storage cnk:temp {data_array[i+10][9]}.slot set from storage cnk:temp {data_array[i+10][9]}.Items[{{id:\"minecraft:{item}\"}}] \n")
                        recipes.append(f"function cnk:recipes/remove with storage cnk:temp {data_array[i+10][9]}\n\n")
                    else:
                        recipes.append(f"data modify storage cnk:temp {data_array[i+10][9]}.slot set from storage cnk:temp {data_array[i+10][9]}.Items[{{components:{{\"minecraft:custom_data\":{{{namespace}:{{ingredient:{{type:\"{item}\"}}}}}}}}}}] \n")
                        recipes.append(f"function cnk:recipes/remove with storage cnk:temp {data_array[i+10][9]}\n\n")

            recipes.append("# sets the colour of the liquid to be output, this is the colour that will also appear in the basin\n")
            recipes.append("# the minecraft wiki has a useful tool for converting colours to decimal format\n")
            recipes.append("# https://minecraft.wiki/w/Data_component_format#custom_model_data\n")
            recipes.append(f"data modify storage cnk:temp {data_array[i+10][9]}.color set value {data_array[i+10][15]}\n")
            recipes.append("\n")
            recipes.append("# sets the callback function that will be called when a player uses a glass bottle on the basin with liquid in it\n")
            recipes.append(f"data modify storage cnk:temp distiller.callback set value \"{data_array[i+10][1]}:{data_array[i+10][9]}/drinks/{data_array[i+10][2]}/main\"\n")
            recipes.append("\n")
            recipes.append("# sets the liquid type, used in the liquid_check functions so must match\n")
            recipes.append(f"data modify storage cnk:temp distiller.liquid set value \"{data_array[i+10][2]}\"\n")
            recipes.append("\n")
            recipes.append("# MUST be called, handles animations and setting the data on the basin\n")
            recipes.append("function cnk:distiller/crafting/finish_distilling")
            
            directory = Path(f"data/{data_array[i+10][1]}/function/distiller/recipes")
            file_path = directory / f"{data_array[i+10][2]}.mcfunction"
            directory.mkdir(parents=True, exist_ok=True)
            with open(file_path, "w", encoding="utf-8") as f:
                f.writelines(recipes)
