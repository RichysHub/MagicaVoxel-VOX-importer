"""
This script imports MagicaVoxel VOX files to Blender.

Usage:
Run this script from "File->Import" menu and then load the desired VOX file.
"""

import os

import bpy
from bpy.props import StringProperty, IntProperty, CollectionProperty
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
                          description="File path used for importing "
                                      "the VOX file",
                          type=bpy.types.OperatorFileListElement)

    directory = StringProperty()

    filename_ext = ".vox"
    filter_glob = StringProperty(
            default="*.vox",
            options={'HIDDEN'},
            )

    start_voxel = IntProperty(name='Start Voxel', default=1, min=1)
    end_voxel = IntProperty(name='End Voxel', default=2, min=2)

    # TODO: float property for scale
    # TODO: float property for voxel size

    def execute(self, context):
        paths = [os.path.join(self.directory, name.name)
                 for name in self.files]
        if not paths:
            paths.append(self.filepath)

        for path in paths:
            import_vox(path, (self.start_voxel, self.end_voxel))
        print('HEY CAN YOU SEE ME?')
        return {'FINISHED'}

    # def draw(self, context):
    #     layout = self.layout
    #     # TODO: options need to be drawn in here
    #     pass


def import_vox(path, bounds):
    start_voxel, end_voxel = bounds
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
            except struct.error as e:
                # end of file
                break
            if name == 'PACK':
                # number of models
                #num_models = struct.unpack('<i', vox.read(4))
                vox.read(4)
            elif name == 'SIZE':
                # model size
                # x, y, z = struct.unpack('<3i', vox.read(12))
                vox.read(12)
            elif name == 'XYZI':
                # voxel data
                # this is the real juicy bit
                num_voxels, = struct.unpack('<i', vox.read(4))
                for voxel in range(num_voxels):
                    voxels.append(struct.unpack('<4B', vox.read(4)))
            elif name == 'RGBA':
                # pallette
                for col in range(256):
                    # palette.update({col+1: struct.unpack('<4B', vox.read(4))})
                    vox.read(4)
            elif name == 'MATT':
                # material
                matt_id, mat_type, weight = struct.unpack('<iif', vox.read(12))

                prop_bits, = struct.unpack('<i', vox.read(4))
                binary = bin(prop_bits)
                # Need to read property values, but this gets fiddly
            else:
                # Any other chunk, we don't know how to handle
                # This puts us out-of-step
                print('Unknown Chunk id {}'.format(name))

    end_voxel = min([end_voxel, len(voxels)])

    for voxel in voxels[start_voxel:end_voxel]:
        location = [float(coord) for coord in voxel[:3]]
        bpy.ops.mesh.primitive_cube_add(radius=0.5, location=location)

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
