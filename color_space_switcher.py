bl_info = {
    "name": "Color Space Switcher",
    "author": "@itsBowl",
    "version": (1, 0),
    "blender": (3, 00, 0),
    "location": "Node Editor",
    "description": "Allows for batch switching of color spaces",
    "warning": "",
    "doc_url": "",
    "category": "Node",
}



import bpy
from bpy.types import (
    AddonPreferences,
    Operator,
    Panel,
    PropertyGroup,
)

def define_color_spaces():
#    Build a list of all available color spaces
    material = ""
    if material not in bpy.data.materials:
        material = bpy.data.materials.new("color_spaces_test_material")
        material.use_nodes = True
    else:
        material = bpy.data.materials["color_spaces_test_material"]
                
 
    texture = material.node_tree.nodes.new("ShaderNodeTexImage")
    texture.image = bpy.data.images.new("test_image", 64, 64)
    spaces = type(texture.image).bl_rna.properties['colorspace_settings'].fixed_type.properties['name'].enum_items
    counter = 0
    color_spaces = []
    for i in spaces:
        text = str(i)
        between_quotes = text.split('"')[1::2]
        new = ((str(between_quotes)[2:-2]), (str(between_quotes)[2:-2]), "")
        color_spaces.append(new)
        counter += 1
    for img in bpy.data.images:
        if img.name[:10] == "test_image":
            bpy.data.images.remove(img)
    for m in bpy.data.materials:
        if m.name == "color_spaces_test_material":
            bpy.data.materials.remove(m)
    return color_spaces


def images_in_tree(node_tree):
#    Builds a list of every image within a material, including all node groups
    for node in node_tree.nodes:
        if hasattr(node, "image"):
            yield node.image
        if hasattr(node, "node_tree"):
            yield from images_in_tree(node.node_tree)
        
        
def color_space_swap(self, context):
#    Swaps the color spaces of every image with specified color space
    con = context.scene.color_switch_spaces
    input_color_space = con.in_color_spaces
    output_color_space = con.out_color_spaces
    for mat in bpy.data.materials:
        image_list = []
        if mat.use_nodes:
            image_list = filter(None, images_in_tree(mat.node_tree))
        for i in image_list:
            if i.colorspace_settings.name == input_color_space:
#                print(f'Found color space {input_color_space} for images {i.name}, swapping color space to {output_color_space}')
                 i.colorspace_settings.name = output_color_space
            


class Col_Switch_Properties(bpy.types.PropertyGroup):
#    Defines the properties of the input and output of the panel
    color_spaces = define_color_spaces()
    in_color_spaces : bpy.props.EnumProperty(
        name="Input",
        items=color_spaces,
    )
    
    out_color_spaces : bpy.props.EnumProperty(
        name="Output",
        items=color_spaces,
    )
    
    
    
#class NODE_PT_MAINPANEL(bpy.types.Panel):
##    Defines the main panel class to draw in the node editor
#    bl_label = "Switch Color Space"
#    bl_idname = "NODE_PT_MAINPANEL"
#    bl_space_type = "NODE_EDITOR"
#    bl_region_type = "UI"
#    bl_category = "Color Space Switcher"
#    
#    def draw(self, context):
#        layout = self.layout
#        
#        row = layout.row()
#        row.operator('node.execute')
        
        
class COL_SWITCH_PT_LAYOUTPANEL(bpy.types.Panel):
#    Defines main panel to draw in the node editor
    bl_label = "Switch Color Space"
    bl_idname = "COL_SWITCH_PT_LayoutPanel"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Color Space Switcher"
    
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        col = layout.column()
        tools = context.scene.color_switch_spaces
        
        layout.operator('node.execute')
        
        #col.label(text="Input Color Space")
        layout.prop(tools, "in_color_spaces")
        
        #col.label(text="Output Color Space")
        layout.prop(tools, "out_color_spaces")
        
        
class NODE_OT_TEST(bpy.types.Operator):
    bl_label = "Swap Color Space"
    bl_idname = "node.execute"
    
    
    def execute(self, context):
        color_space_swap(self, context)
        
        return {"FINISHED"}
    
classes = [NODE_OT_TEST,
        COL_SWITCH_PT_LAYOUTPANEL,
        Col_Switch_Properties,
        ]
        
def register():
    for i in classes:
        bpy.utils.register_class(i)
    bpy.types.Scene.color_switch_spaces = bpy.props.PointerProperty(type=Col_Switch_Properties)
    
def unregister():
    for i in classes:
        bpy.utils.unregister_class(i)
    del bpy.types.Scene.color_switch_spaces
    
if __name__ == "__main__":
    register()