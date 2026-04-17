# cnk-addon-item-generator
I hate making 12ish files everytime I need to add a single item to my CNK addon so here is a script that does it for me yay!


This is for [CNK Addon Dev](https://github.com/maybejake/crop-and-kettle).

This script regenerates all the files rather than adds new ones in order to keep the font index functional. There is a limit of 999 items.
### To Use
- To use this you need to download and edit the cnk_item_addon.xlsx and fill it with the items you want to be generated.
- Then export the spreadsheet as a .csv
- The script will read from the csv placed in the same directory as the script to generate the items
- Run the script with python
- The items will either be output in a folder or will be automatically moved into your back

### Working with the spreadsheet
#### Settings
- **Dynamic Insertion** attempts to insert the generated files into their proper file paths in a datapack in the same directory
- **Backups** will backup the old files if Dynamic Insertion is enables
- **Datapack Place** is the location of the datapack in relation to the the script. **Within** is where the data and assets folder are in the same directory as the script and **External** is where the pack folder is in the same directory as the script
#### Items
- The **Index** is a number that is assigned to each item for the font sheet
- The **Namespace** is self explanitory, the addon name
- The **ID** is the identifier for the item
- The **Name** is the translation key that the player sees
- The **Type** indicates the unlock notification type, if that be recipe or ingredient
- **Nutrition** and **Saturation** are just for the item nutrition and saturation
- The **Loot Group** is the loot table subfolder that the item will be placed into. If none is specified, it will go into a 'unspecified_group' folder
- _The following should only be included if the item is craftable by recipe_
- The **Category** is the cookbook category the item's recipe will appear in. Use **distiller_book** if the item is brewed
- The **Workstation** is the workstation where the item is crafted
- The Ingredients (**Ing1**, **Ing2**, **Ing3** ...) are the ingredients used to craft the item. If the item is crafted with a cutting board, only the first item will be considered
- The **Color** is only to describe the color of brewed drinks in [decimal form](https://minecraft.wiki/w/Data_component_format#custom_model_data)
- The **Ages** boolean describes if the outputted item should act like wines where they can be aged
- The **Custom Station Proccess** points to the folder where the custom worstation's processing happens. For example, with the mortar_and_pestle, it is 'mash'
- The **Distill Lock** describes the time it takes to distill an recipe. This is indicated with a value and a prefix. '15s' is 15 seconds, the normal short_lock for the distiller. '20m' is 20 minutes, the normal lock for the distiller. '5d' is 5 days, a custom lock time that will be generated. '1d' = '20m' = '1200s'
