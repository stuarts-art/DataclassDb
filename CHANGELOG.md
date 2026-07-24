# Changelog

* DataclassDb is still in Beta. On release, this section may be consolidated.

## [Unreleased]

## [0.1.8] - 2026-07-23

* Added "verify_table" flag to DataclassDb to optionally skip checking if the table exists or needs updates.

## [0.1.7] - 2026-07-23

* Add get_all

## [0.1.6] - 2026-07-20

* Fixed bug where primary generated primary key would be regenerated for repeat unique inserts.
* Solidified insert returning:
  * If there is a primary key, return the primary key
  * Else return the rowid
  * *Note*: that insert many does not return anything.

## [0.1.5] - 2026-07-19

* Added support for `**kwargs` in DataclassDb contains and get.
* Better insertion resolution when both unique and primary key cols are in the same table.
* Added initial scaffolding for docs.

## [0.1.4] - 2026-07-15

### New Feature

* [Issue 3] - Added `execute_many` and `insert_many`.
  * [unit tests](https://github.com/stuarts-art/DataclassDb/blob/5d44cbad2f3a5e9251a6735de92e55b72d1bc371/tests/test_dataclass_db.py#L264-L297)
  * 100% Coverage, 100% tests passed [Test Job](https://github.com/stuarts-art/DataclassDb/actions/runs/29433673472/job/87414775773)

## [0.1.3] - 2026-07-14

### Fixed

* [Issue 2] - Fixed bug where tables would always be overwritten if there were table constraints.

## [0.1.2] - 2026-07-14

* Fixed logger bug causing table creation to fail.

## [0.1.1] - 2026-07-13

* [Issue 1] - Added support for nested origin types

[Unreleased]: https://github.com/stuarts-art/DataclassDb/compare/v0.1.8...HEAD
[0.1.8]: https://github.com/stuarts-art/DataclassDb/compare/v0.1.7..v0.1.8
[0.1.7]: https://github.com/stuarts-art/DataclassDb/compare/v0.1.6..v0.1.7
[0.1.6]: https://github.com/stuarts-art/DataclassDb/compare/v0.1.5..v0.1.6
[0.1.5]: https://github.com/stuarts-art/DataclassDb/compare/v0.1.4..v0.1.5
[0.1.4]: https://github.com/stuarts-art/DataclassDb/compare/v0.1.3..v0.1.4
[0.1.3]: https://github.com/stuarts-art/DataclassDb/compare/v0.1.2..v0.1.3
[0.1.2]: https://github.com/stuarts-art/DataclassDb/compare/v0.1.1..v0.1.2
[0.1.1]: https://github.com/stuarts-art/DataclassDb/compare/v0.1.0...v0.1.1
[Issue 1]: https://github.com/stuarts-art/DataclassDb/issues/1
[Issue 2]: https://github.com/stuarts-art/DataclassDb/issues/2
[Issue 3]: https://github.com/stuarts-art/DataclassDb/issues/3
