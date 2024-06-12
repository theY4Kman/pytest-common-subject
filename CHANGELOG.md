# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [Unreleased]


## [1.1.1] — 2024-06-12
### Fixed
 - Resolve `TypeError` in Python versions below 3.10 (due to usage of pipe unions in annotations)
 - (minor) Include tox install command script in source dist


## [1.1.0] — 2024-06-03
### Added
 - Introduce `AsyncCommonSubjectTestMixin` for async tests

### Changed
 - Drop support for Python 3.6 and 3.7 (both EOL) — minimum Python version is now 3.8
 - Support pytest versions 7.2 to 8.2 (and relax version pinning to allow all 8.x versions)


## [1.0.6] — 2022-05-15
### Changed
 - Support pytest versions 7.0 and 7.1 (and relax version pinning to allow all 7.x versions)


## [1.0.5] — 2020-11-12
### Changed
 - Support pytest version 6.1 (and relax version pinning to allow all 6.x versions)


## [1.0.4] - 2020-08-25
### Changed
 - Transferred ownership to @theY4Kman


## [1.0.3] - 2020-08-03
### Fixed
 - Register `precondition` mark to avoid pytest warning

### Changed
 - Include tests, LICENSE, and CHANGELOG in source distribution


## [1.0.2] - 2020-08-01
 - Support pytest versions 4.6, 5.0, 5.1, 5.2, 5.3, 5.4, and 6.0


## [1.0.1] - 2019-05-26
 - Support pytest versions 4.0, 4.4, and 4.5


## [1.0.0] - 2019-04-22
 - Initial release
