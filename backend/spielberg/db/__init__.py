from spielberg.constants import DBType

from .base import BaseDB
from .sqlite.db import SQLiteDB


db_types = {
    DBType.SQLITE: SQLiteDB,
}


def load_db(db_type: DBType) -> BaseDB:
    if db_type not in db_types:
        raise ValueError(
            f"Unknown DB type: {db_type}, Valid db types are: {[db_type.value for db_type in db_types]}"
        )

    return db_types[db_type]()
