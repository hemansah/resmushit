# Changelog

## [1.0.1] - 2024-05-04
### Fixes
- Fixed image extension showing `None` caused by `imghdr`.

### Added
- Added tests with pytest.
- Added `filetype` library to check image file extensions instead of `imghdr`.

### Removed
- Removed dependency of `imghdr` as it is deprecated.
- Removed `colorama` to decrease dependency of external libraries.

## [1.0.0] - 2024-04-13

### Added
 - Initial Release