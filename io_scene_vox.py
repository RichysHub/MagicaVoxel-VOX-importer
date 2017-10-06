"""
This script imports MagicaVoxel VOX files to Blender.

Usage:
Run this script from "File->Import" menu and then load the desired VOX file.
"""

# <pep8 compliant>

import os

import bpy
from bpy.props import StringProperty, IntProperty, FloatProperty, BoolProperty, CollectionProperty
from bpy_extras.io_utils import ImportHelper

import struct

bl_info = {
    "name": "MagicaVoxel VOX format",
    "author": "Richard Spencer",
    "blender": (2, 74, 0),
    "location": "File > Import-Export",
    "description": "Import MagicaVoxel .vox files",
    "warning": "",
    "wiki_url": "",
    "support": 'TESTING',
    "category": "Import-Export"}


class ImportVOX(bpy.types.Operator, ImportHelper):
    """Load a MagicaVoxel VOX File"""
    bl_idname = "import_scene.vox"
    bl_label = "Import VOX"
    bl_options = {'PRESET', 'UNDO'}

    files = CollectionProperty(name="File Path",
                               description="File path used for importing the VOX file",
                               type=bpy.types.OperatorFileListElement)

    directory = StringProperty()

    filename_ext = ".vox"
    filter_glob = StringProperty(
            default="*.vox",
            options={'HIDDEN'},
            )

    voxel_spacing = FloatProperty(name="Voxel Spacing", default=1.0)
    voxel_size = FloatProperty(name="Voxel Size", default=1.0)

    use_bounds = BoolProperty(name="Use Voxel Bounds", default=False)

    start_voxel = IntProperty(name="Start Voxel", default=1, min=1)
    end_voxel = IntProperty(name="End Voxel", default=20, min=2)

    def execute(self, context):
        paths = [os.path.join(self.directory, name.name)
                 for name in self.files]
        if not paths:
            paths.append(self.filepath)

        keywords = self.as_keywords(ignore=("files", "filepath", "directory", "filter_glob",))

        for path in paths:
            import_vox(path, **keywords)
        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "voxel_spacing")
        layout.prop(self, "voxel_size")
        layout.prop(self, "use_bounds")
        if self.use_bounds:
            layout.prop(self, "start_voxel")
            layout.prop(self, "end_voxel")


def import_vox(path, *, voxel_spacing=1, voxel_size=1, use_bounds=False, start_voxel=None, end_voxel=None):
    import time
    time_start = time.time()

    with open(path, 'rb') as vox:

        voxels = []
        palette = {}

        # assert is VOX 150 file
        assert (struct.unpack('<4ci', vox.read(8)) == (b'V', b'O', b'X', b' ', 150))

        # MAIN chunk
        assert (struct.unpack('<4c', vox.read(4)) == (b'M', b'A', b'I', b'N'))
        N, M = struct.unpack('<ii', vox.read(8))
        assert (N == 0)  # MAIN chunk should have no content

        # M is remaining # of bytes in file

        while True:
            try:
                *name, s_self, s_child = struct.unpack('<4cii', vox.read(12))
                assert (s_child == 0)  # sanity check
                name = b''.join(name).decode('utf-8')  # unsure of encoding..
            except struct.error:
                # end of file
                break
            if name == 'PACK':
                # number of models
                num_models = struct.unpack('<i', vox.read(4))
            elif name == 'SIZE':
                # model size
                # x, y, z = struct.unpack('<3i', vox.read(12))
                vox.read(12)
            elif name == 'XYZI':
                # voxel data
                num_voxels, = struct.unpack('<i', vox.read(4))
                for voxel in range(num_voxels):
                    voxel_data = struct.unpack('<4B', vox.read(4))
                    voxels.append(voxel_data)
            elif name == 'RGBA':
                # palette
                for col in range(256):
                    palette.update({col+1: struct.unpack('<4B', vox.read(4))})
            elif name == 'MATT':
                # material
                matt_id, mat_type, weight = struct.unpack('<iif', vox.read(12))

                prop_bits, = struct.unpack('<i', vox.read(4))
                binary = bin(prop_bits)
                # Need to read property values, but this gets fiddly
                # TODO: finish implementation
            else:
                # Any other chunk, we don't know how to handle
                # This puts us out-of-step
                print('Unknown Chunk id {}'.format(name))
                return {'CANCELLED'}

    if use_bounds:
        # clamp end_voxel to size of model
        end = min([end_voxel, len(voxels)])
        voxels = voxels[start_voxel:end]

    used_palette_indices = set()
    for voxel in voxels:
        # This is done here, so to avoid adding materials for voxels not in bounds
        used_palette_indices.add(voxel[3])  # record the pallette entry is used

    mat_palette = {}

    for index in used_palette_indices:
        palette_entry = palette[index]
        material = bpy.data.materials.new("Voxel_mat{}".format(index))
        material.diffuse_color = [col/255 for col in palette_entry[:3]]
        material.diffuse_intensity = 1.0
        material.alpha = palette_entry[3]
        mat_palette.update({index: material})

    # peel first voxel information
    voxel, *voxels = voxels
    location = [float(coord) * voxel_spacing for coord in voxel[:3]]
    # Using primitive_cube_add once here, to give us a template cube
    bpy.ops.mesh.primitive_cube_add(radius=0.5 * voxel_size, location=location)
    base_voxel = bpy.context.object
    base_voxel.active_material = mat_palette[voxel[3]]

    to_link = []

    for voxel in voxels:
        copy = base_voxel.copy()
        copy.data = base_voxel.data.copy()
        copy.location = [float(coord)*voxel_spacing for coord in voxel[:3]]
        to_link.append(copy)
        copy.active_material = mat_palette[voxel[3]]

    for object_ in to_link:
        bpy.context.scene.objects.link(object_)

    bpy.context.scene.update()

    print('\nSuccessfully imported {} in {:.3f} sec'.format(path, time.time() - time_start))
    return {'FINISHED'}


def menu_func_import(self, context):
    self.layout.operator(ImportVOX.bl_idname, text="MagicaVoxel (.vox)")


def register():
    bpy.utils.register_module(__name__)
    bpy.types.INFO_MT_file_import.append(menu_func_import)


def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.INFO_MT_file_import.remove(menu_func_import)


if __name__ == "__main__":
    register()
