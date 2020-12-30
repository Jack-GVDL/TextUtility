from Lib import *


# operation
# create and config component
component_text_1 = UtilText_Text()
component_text_2 = UtilText_Text()
component_text_3 = UtilText_Text()

component_text_1.setData({"text": ["text 1"]})
component_text_2.setData({"text": ["text 2"]})
component_text_3.setData({"text": ["text 3"]})

component_list = UtilText_List()
component_list.addChild(component_text_1)
component_list.addChild(component_text_2)
component_list.addChild(component_text_3)

# render
content: str = component_list.render()
print("-----")
print(content, end='')
print("-----")
