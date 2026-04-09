# sets the page number from the current global, MUST be present
execute store result storage cnk:temp register.page_number int 1 run scoreboard players get $global_distiller_book_page cnk.dummy

# sets the page name
data modify storage cnk:temp register.page_name set value "item.spiced.ethanol"

# sets the ingredients
data modify storage cnk:temp register.ingredients set value [ \
    {key:"item.minecraft.water", font:"cnk.book:icons"}, \
    {key:"item.cnk.corn", font:"cnk.book:icons"}, \
    {key:"item.cnk.cooking_oil", font:"cnk.book:icons"} \
]

data modify storage cnk:temp register.source set value {key:"spiced.source", font:"spiced:icons"}

# register the page
function cnk:cookbook/pages/register
