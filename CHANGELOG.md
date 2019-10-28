# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and from v2.2.1 this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
## [Unreleased]


## [2.2.1] - 2019-10-28
### Added
- Added [CHANGELOG](CHANGELOG.md) to help document changes made to this importer.

### Changed
- Tags of versions changed to [Semantic Versioning](https://semver.org/). This adds the `patch` field, so that simple bug fixes are not conflated with new functionality.
- Updated [README](README.md) to help new users install the add-on, and to serve as a usage guide.

### Fixed
- README typos, and several occurrences of `.vox` without markdown.


## [2.2] - 2019-10-17
### Added
- Option to join voxels together into a single Blender object.


## [2.1] - 2019-10-7
### Added
- Option `Animation frame to load` to import a single frame of an animated model. Defaults to first frame.

### Changed
- Importing an animated model will now only import 1 frame, not all frames combined.


## [2.0] - 2019-10-4
### Changed
- Updated to work with Blender 2.80. Incompatible Blender API changes meant the previous version was non-functional.
- `Use Shadeless Materials` option now makes imported materials of type `Emission` due to removal of previous Blender option.

### Removed
- Support for Blender 2.7x has ended as of this version due to API changes, and a perceived lack of utility in supporting both.


## [1.0] - 2019-10-4
### Fixed
- Corrected `MATT` chunk skipping code to prevent chunk misalignment when importing.
- `Use Voxel Bounds` behaviour was previously incorrect due to an off-by-one error, this has been fixed.
- Behaviour of default palette was reverted to the state prior to v0.7, as that change was seen to be in error.

### Deprecated
- This is the last version that will support Blender 2.7x for the foreseeable future. Moving to Blender 2.80's new API will be a considerate change, and supporting both is not simple.


## [0.9] - 2018-03-15
### Added
- Added [LICENSE](LICENSE)


## [0.8] - 2017-10-25
### Added
- [README](README.md) added, explaining motivation and features.


## [0.7] - 2017-10-19
### Fixed
- Behaviour of default palette was changed in an attempt to rectify miscolored imports.


## [0.6] - 2017-10-18
### Added
- Default palette is now supported, as per format specification. This will only affect files for which no palette chunk is present.


## [0.5] - 2017-10-07
### Added
- Added `Use Shadeless Materials` option. Enables the `use_shadeless` Blender property so that materials imported from `.vox` files are insensitive to light or shadow.
- Added gamma correction to imported material colors, so that they are reproduced in Blender correctly.
- Added `Gamma Correction Value` option, in case a use case requires a different value.
- Added `Gamma Correct Colors` option to disable gamma correction behaviour.

### Changed
- Gamma correction changes the resultant imported material colors.


## [0.4] - 2017-10-06
### Added
- Palette is now read from `.vox` files, creating diffuse Blender materials.
- Added `Use Palette Colors` option. Disabling this will skip material creation.


## [0.3] - 2017-10-05
### Changed
- Large performance boon, as Blender cube creation is now managed with `clone` operations.


## [0.2] - 2017-10-05
### Added
- Added `Voxel Spacing` option. Sets distance between neighbouring voxels, in Blender units.
- Added `Voxel Size` option. Scales the resulting Blender cubes to have side length equal to `Voxel Size`.
- Import options are now manually controlled by defining `ImportVox.draw`.
- Option `Use Voxel Bounds` added, checkbox which enables `Start Voxel` and `End Voxel` options.
- Time to import is now printed into the Blender console.

### Changed
- `Start Voxel` and `End Voxel` options are not enabled by default, so default behaviour is to import entire file.


## [0.1] - 2017-10-03
### Added
- Primary working version of import script
- `Start Voxel` and `End Voxel` options added, which take a subset of the `.vox` file contents, for importing very large models.


[Unreleased]: https://github.com/olivierlacan/keep-a-changelog/compare/v2.2.1...HEAD
[2.2.1]: https://github.com/RichysHub/MagicaVoxel-VOX-importer/compare/v2.2...v2.2.1
[2.2]: https://github.com/RichysHub/MagicaVoxel-VOX-importer/compare/v2.1...v2.2
[2.1]: https://github.com/RichysHub/MagicaVoxel-VOX-importer/compare/v2.0...v2.1
[2.0]: https://github.com/RichysHub/MagicaVoxel-VOX-importer/compare/v1.0...v2.0
[1.0]: https://github.com/RichysHub/MagicaVoxel-VOX-importer/compare/v0.9...v1.0
[0.9]: https://github.com/RichysHub/MagicaVoxel-VOX-importer/compare/v0.8...v0.9
[0.8]: https://github.com/RichysHub/MagicaVoxel-VOX-importer/compare/v0.7...v0.8
[0.7]: https://github.com/RichysHub/MagicaVoxel-VOX-importer/compare/v0.6...v0.7
[0.6]: https://github.com/RichysHub/MagicaVoxel-VOX-importer/compare/v0.5...v0.6
[0.5]: https://github.com/RichysHub/MagicaVoxel-VOX-importer/compare/v0.4...v0.5
[0.4]: https://github.com/RichysHub/MagicaVoxel-VOX-importer/compare/v0.3...v0.4
[0.3]: https://github.com/RichysHub/MagicaVoxel-VOX-importer/compare/v0.2...v0.3
[0.2]: https://github.com/RichysHub/MagicaVoxel-VOX-importer/compare/v0.1...v0.2
[0.1]: https://github.com/RichysHub/MagicaVoxel-VOX-importer/releases/tag/v0.1
