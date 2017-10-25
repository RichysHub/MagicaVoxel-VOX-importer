# MagicaVoxel-VOX-importer
Blender import script for ![MagicaVoxel .vox format](https://github.com/ephtracy/voxel-model/blob/master/MagicaVoxel-file-format-vox.txt).

# Motivation
VoxelShop, MagicaVoxel and other voxel editing software are great to quickly create voxel models.
However, at the time of this scripts creation, no workflow existed to import models to blender, 
retaining the internal voxel geometry, only as a .dae shell.

This script imports each voxel of the original model as an individual cube primitive, which allows for easy physics simulations.

![Example Physics Simulation](https://i.imgur.com/r0EwHFO.gif)

# Features
* Material generation based on palette colors
* Default palette support
* Gamma corrected colors
* Import scale options
* Partial import for large models
* Shadeless material option

# Intended Future Features
* Full material support for glass, metal, and emission type voxels
