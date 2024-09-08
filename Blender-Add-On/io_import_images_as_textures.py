''' 
    ====================================================================================================

    Import Images as Textures

    ===========================

    This addon is meant for batch importing of images to be used as textures. 
    I needed this primarily for importing large sets of images to be used as brush textures.
    Lots of great ideas stolen from the built-in Images as Planes addon and by the Import Brush Set addon by Daniel Grauer (kromar), CansecoGPC

    ===========================

    Copyright (C) Andrew Frueh, 2022
    This content is under the GNU General Public License. 

    ==================================================================================================== 
'''


# ==========================================================
# Header

bl_info = {
    "name": "Import Images as Textures",
    "author": "Andrew Frueh",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "location": "File > Import > Images as Textures or Add > Mesh > Images as Textures",
    "description": "Imports images and creates textures with the desired settings. "
                   "Usefull for brush textures, etc.",
    "warning": "",
    "wiki_url": "",
    "category": "Import-Export",
    }


# ==========================================================
# Functionallity

# Import Blender base-class
import bpy
#
from bpy.props import *
# import the path library (for parsing the filename)
import pathlib

# Only create an Image data block if loaded file is one of these types
#   using bpy.types.Image.file_format [‘BMP’, ‘IRIS’, ‘PNG’, ‘JPEG’, ‘JPEG2000’, ‘TARGA’, ‘TARGA_RAW’, ‘CINEON’, ‘DPX’, ‘OPEN_EXR_MULTILAYER’, ‘OPEN_EXR’, ‘HDR’, ‘TIFF’, ‘WEBP’, ‘AVI_JPEG’, ‘AVI_RAW’, ‘FFMPEG’], default ‘TARGA’
ALLOWED_FILE_TYPES = ['PNG', 'JPEG', 'JPEG2000', 'BMP', 'TIFF']

# Define an Operator (the dialog box)
class CustomDialog(bpy.types.Operator):
    # Choose a unique ID (note, at the scope of 'bpy.ops' e.g. 'bpy.ops.import.file_selector')
    bl_idname = "import_image.to_texture"
    # In the context of a "fileselect" dialog, label is used for the "okay" button
    bl_label = "Import Images as Textures"

    # Define the fields used by the Operator
    directory: bpy.props.StringProperty(subtype="FILE_PATH")
    files: bpy.props.CollectionProperty(type=bpy.types.OperatorFileListElement, options={'HIDDEN', 'SKIP_SAVE'})

    # ==========================
    # Properties

    # General attributes
    useNamePrePost : BoolProperty(name="Use name prefix / suffix", default=False, description="Prepend / append strings to each Texture name.")
    namePre : StringProperty(name="Name Prefix", description="Prepend this to the front of each Texture name.")
    namePost : StringProperty(name="Name Suffix", description="Append this to the end of each Texture name.")

    # Image attributes
    imgProp_fakeUser : BoolProperty(name="Fake User", default=True, description="Assign 'Fake User' to each new Image to keep them safe from garbage collection.")
    imgProp_useExisting : BoolProperty(name="Use Existing Image", default=True, description="If image already exists with this Blend file, use it.")

    # Texture attributes
    texture_use_calculate_alpha : BoolProperty(name="Calculate Alpha", default=True, description="Use 'Calculate Alpha' which treats gray value as alpha chanel.")
    texture_invert_alpha : BoolProperty(name="Invert Alpha", default=False, description="Invert the alpha chanel.")
    texture_use_fake_user : BoolProperty(name="Fake User", default=True, description="Assign 'Fake User' to each new Texture to keep them safe from garbage collection.")
    texture_use_interpolation : BoolProperty(name="Interpolation", default=True, description="Interpolation is on by default, but turning it off gives you true pixelated textures.")
    texture_use_mipmap : BoolProperty(name="Mipmap", default=True, description="MIP maps are good for object textures, but for brushes they are unnecessary and increase the file size.")
 
    # ==========================
    # Draw section (UI layout)

    # Draw sub-routine
    def draw_general_attributes(self, context):
        # Standard draw references
        box = self.layout.box()

        box.prop(self, "useNamePrePost")
        col = box.column()
        row = col.row()
        row.prop(self, "namePre")
        row = col.row()
        row.prop(self, "namePost")
        col.enabled = self.useNamePrePost

    # Draw sub-routine
    def draw_image_attributes(self, context):
        # Standard draw references
        box = self.layout.box()

        box.label(text="Attributes for Images:", icon='IMAGE')
        box.prop(self, "imgProp_fakeUser")
        box.prop(self, "imgProp_useExisting")

    # Draw sub-routine
    def draw_texture_attributes(self, context):
        # Standard draw references
        box = self.layout.box()

        box.label(text="Attributes for Textures:", icon='TEXTURE')
        box.prop(self, "texture_use_calculate_alpha")
        box.prop(self, "texture_invert_alpha")
        box.prop(self, "texture_use_fake_user")
        box.prop(self, "texture_use_interpolation")
        box.prop(self, "texture_use_mipmap")

    # Main draw call
    def draw(self, context):
        self.draw_general_attributes(context)
        self.draw_image_attributes(context)
        self.draw_texture_attributes(context)
        
    # ==========================
    # Core functionallity

    # Operator.invoke is called when the operator is invoked (startup)
    def invoke(self, context, event):
        # Tell the WindowManager to open a file-select dialog box: fileselect_add(operator)
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    # Operator.execute is called when the user clicks the "okay" button
    def execute(self, context):
        CustomFunctionallity(self,context)
        return {'FINISHED'}

# Define the custom functionallity to be called by the button in the panel
def CustomFunctionallity(self, context):
    for file in self.files:
        LoadImageAsTexture(file,self)

# Single image loader, called from loop above
def LoadImageAsTexture(file,self):

    # Get the simplified name for the texture (filename without extension)
    simpleName = pathlib.Path(file.name).stem

    # Should we add strings to the name?
    if self.useNamePrePost == True:
        # Add strings to the name (both pre and post)
        simpleName = self.namePre + simpleName + self.namePost

    # Load the image to be used by the texture
    image = bpy.data.images.load(self.directory+file.name, check_existing=self.imgProp_useExisting)
    image.use_fake_user = self.imgProp_fakeUser
    image.name = simpleName

    # I don't love this weird shorthand. I can't believe you can write this... but at least it works.
    if any( image.file_format == fileType for fileType in ALLOWED_FILE_TYPES ):

        # Create the texture (of type IMAGE)
        texture = bpy.data.textures.new(simpleName, 'IMAGE')
        texture.use_calculate_alpha = self.texture_use_calculate_alpha
        texture.invert_alpha = self.texture_invert_alpha
        texture.use_fake_user = self.texture_use_fake_user
        texture.use_interpolation = self.texture_use_interpolation
        texture.use_mipmap = self.texture_use_mipmap

        # Link the image to the texture
        bpy.data.textures[texture.name].image = image

        # Report success
        self.report({'INFO'}, "Load success! Texture '"+simpleName+"' created.")

    else:
        # Clean up / delete the image data block as it is linked to bad data
        bpy.data.images.remove(image)
        # Loaded file is not an allowed file type, undo image creation
        self.report({'INFO'}, "Load fail:"+file.name+" - No texture created")
       

# Handler function called by the menu item (appended below)
def reference_to_operator(self, context):
    # We store a reference to the Operator in self.layout. "text" is the name used in the menu.
    self.layout.operator(CustomDialog.bl_idname, text="Images as Textures", icon='TEXTURE')


# ==========================================================
# Registration

# List the classes to be registered/unregistered below
classes = (CustomDialog,)

# Define the registration function (called by Blender)
def register():
    # Register the classes listed above
    for cls in classes:
       bpy.utils.register_class(cls)
    # Append this addon to the menu
    bpy.types.TOPBAR_MT_file_import.append(reference_to_operator)
    bpy.types.VIEW3D_MT_image_add.append(reference_to_operator)

# Define the unregistration function (called by Blender)
def unregister():
    # Unregister the classes listed above
    for cls in classes:
        bpy.utils.unregister_class(cls)
    # Remove this addon from the menu
    bpy.types.TOPBAR_MT_file_import.remove(reference_to_operator)
    bpy.types.VIEW3D_MT_image_add.remove(reference_to_operator)


# If the scope is correct, run registration (do we need this?)
if __name__ == "__main__":
    register()

# OEF