from Source import *


# operation
# create and config component
component_text_title_1 = UtilText_Text()
component_text_title_2 = UtilText_Text()
component_text_title_3 = UtilText_Text()
component_text_title_4 = UtilText_Text()
component_text_1_1 = UtilText_Text()
component_text_1_2 = UtilText_Text()
component_text_1_3 = UtilText_Text()
component_text_2_1 = UtilText_Text()
component_text_2_2 = UtilText_Text()
component_text_2_3 = UtilText_Text()

component_text_title_1.setData({"text": ["title 1"]})
component_text_title_2.setData({"text": ["title 2"]})
component_text_title_3.setData({"text": ["title 3"]})
component_text_title_4.setData({"text": ["title 4"]})
component_text_1_1.setData({"text": ["text 1 1"]})
component_text_1_2.setData({"text": ["text 1 2"]})
component_text_1_3.setData({"text": ["text 1 3"]})
component_text_2_1.setData({"text": ["text 2 1"]})
component_text_2_2.setData({"text": ["text 2 2"]})
component_text_2_3.setData({"text": ["text 2 3"]})

# list
component_text_list_1 = UtilText_Text()
component_text_list_2 = UtilText_Text()
component_text_list_3 = UtilText_Text()

component_text_list_1.setData({"text": ["text 1"]})
component_text_list_2.setData({"text": ["text 2"]})
component_text_list_3.setData({"text": ["text 3"]})

component_list_1 = UtilText_List()
component_list_1.addChild(component_text_list_1)
component_list_1.addChild(component_text_list_2)
component_list_1.addChild(component_text_list_3)

# combine
component_table_1 = UtilText_Table()
component_table_1.addRow([component_text_title_1, component_text_title_2, component_text_title_3, component_text_title_4])
component_table_1.addRow([component_text_1_1, component_text_1_2, component_text_1_3, component_list_1])
component_table_1.addRow([component_text_2_1, component_text_2_2, component_text_2_3])

# render
content: str = component_table_1.render()
print("-----")
print(content, end='')
print("-----")
