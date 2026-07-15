from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Annotated

from dataclassdb.dataclass_db import DataclassDb
from dataclassdb.dataclass_field_codec import (
    DatetimeIntCodec,
    DatetimeTextCodec,
)


class TestDateTextCodec:
    @dataclass
    class ClassOne:
        id: Annotated[int, "PRIMARY KEY"]
        test_00: datetime
        test_01: datetime | None
        test_02: Annotated[datetime | None, "NOT NULL"]
        updated: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
        created: Annotated[
            datetime | None,
            "NOT NULL",
            "ON CONFLICT IGNORE",
            "DEFAULT CURRENT_TIMESTAMP",
        ] = None

    def test_class_init(self, db_mem_connection):
        dt = datetime.now(tz=timezone.utc)
        obj_0 = self.ClassOne(0, dt, dt, dt)
        assert obj_0
        with DataclassDb(self.ClassOne, db_mem_connection) as db:
            for t in ["test_00", "test_01", "test_02"]:
                assert t in db.codec.class_fields
                class_field = db.codec.class_fields[t]
                assert class_field.sql_type == "TEXT"
                assert isinstance(class_field.codec, DatetimeTextCodec)
            inserted = db.insert(obj_0)
            assert inserted
            print(f"inserted {inserted}")
            obj = db.get(0)
            print(f"obj {obj}")
            assert obj.id is not None
            assert obj.test_00 is not None
            assert obj.test_01 is not None
            assert obj.test_02 is not None
            assert obj.updated is not None
            assert obj.created is not None
            print(obj)

            dt = datetime.now(tz=timezone.utc)
            obj_0_changed = self.ClassOne(0, dt, dt, dt)
            inserted = db.insert(obj_0_changed)
            obj_changed = db.get(0)
            assert obj_changed.test_00 != obj.test_00
            assert obj_changed.test_01 != obj.test_01
            assert obj_changed.test_02 != obj.test_02
            assert obj_changed.test_02 != obj.test_02
            assert obj_changed.updated != obj.updated
            assert obj_changed.created == obj.created
            assert db.codec.class_fields["test_00"].encode(None) is None
            assert db.codec.class_fields["test_00"].decode(None) is None


class TestDateIntegerCodec:
    @dataclass
    class ClassOne:
        id: Annotated[int, "PRIMARY KEY"]
        test_00: Annotated[datetime, "INTEGER"]
        updated: Annotated[datetime | None, "INTEGER", "DEFAULT (unixepoch())"] = field(
            default_factory=lambda: datetime.now(timezone.utc)
        )
        created: Annotated[datetime | None, "INTEGER", "DEFAULT (unixepoch())"] = None

    def test_class_init(self, db_mem_connection):
        dt = datetime.now(tz=timezone.utc)
        obj_0 = self.ClassOne(0, dt)
        assert obj_0
        with DataclassDb(self.ClassOne, db_mem_connection) as db:
            for t in ["test_00", "updated", "created"]:
                assert t in db.codec.class_fields
                class_field = db.codec.class_fields[t]
                assert class_field.sql_type == "INTEGER"
                assert isinstance(class_field.codec, DatetimeIntCodec)
            inserted = db.insert(obj_0)
            assert inserted
            print(f"inserted {inserted}")
            get_obj = db.get(0)
            assert get_obj
            assert get_obj.id is not None
            assert get_obj.test_00
            assert get_obj.updated
            assert get_obj.created

            obj_0_changed = self.ClassOne(0, dt)
            obj_0_changed.test_00 += timedelta(seconds=1)
            obj_0_changed.updated += timedelta(seconds=1)
            assert obj_0_changed.updated != obj_0.updated

            inserted = db.insert(obj_0_changed)
            assert inserted
            get_changed_obj = db.get(0)
            assert get_changed_obj

            assert get_changed_obj.id is not None
            assert get_changed_obj.test_00
            assert get_changed_obj.updated
            assert get_changed_obj.created
            assert obj_0 != get_changed_obj
            assert db.codec.class_fields["test_00"].encode(None) is None
            assert db.codec.class_fields["test_00"].decode(None) is None
            assert get_obj.updated != get_changed_obj.updated
            assert get_obj.created == get_changed_obj.created
