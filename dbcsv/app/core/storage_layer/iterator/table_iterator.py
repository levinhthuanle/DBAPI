

from pathlib import Path
import csv
import os
import json
from typing import List, Any

from dbcsv.app.core.storage_layer.datatypes import DBTypeObject

DB_DIR = str(Path(__file__).parent.parent.parent.parent.parent / "data")

class TableIterator:
    def stream_json(self):
        yield '{\n'
        yield f'"table_name": "{self.table_name}",\n'
        yield f'"columns": {json.dumps(self._columns)},\n'
        yield f'"column_types": {json.dumps(self._column_types)},\n'
        yield '"data": [\n'

        first = True
        for batch in self:
            row_json = json.dumps(batch)
            if first:
                yield row_json
                first = False
            else:
                yield ',\n' + row_json

        yield '\n]\n}'

    
    # path: schema/table_name
    def __init__(self, schema: str, table: str, metadata: dict[str, str] = None, batch_size: int = 1000, limit: int = None) -> None:
        self.schema = schema.lower()
        self.table_name = table.lower()
        self.batch_size = batch_size
        self._columns = list(metadata.keys()) if metadata else []
        self._column_types = list(metadata.values()) if metadata else []
        self._file = self._load_file(schema=self.schema, table=self.table_name)
        self._reader = csv.reader(self._file)
        self._check_header()
        self._is_done = False
        self._cache: List[List[Any]] = []
        self._used: List[List[Any]] = []
        self.limit = limit
        self.row_count = 0
        
    
    def __iter__(self) -> 'TableIterator':
        return self
    
    def _load_next_batch(self) -> List[List[Any]]:
        self._cache = []
        for _ in range(self.batch_size):
            try:
                row = next(self._reader)
                row = DBTypeObject.convert_type(row, self._column_types)
                
                if len(row) != len(self._columns):
                    raise ValueError(f"Row length does not match column length in {self.schema}/{self.table_name}.")
                self._cache.append(row)
            except StopIteration:
                self._is_done = True
                break
    
    def __next__(self) -> List[List[Any]]:
        if not self._cache and not self._is_done:
            self._load_next_batch()

        if self._cache:
            self._used.append(self._cache[0])
            return self._cache.pop(0)
        else:
            self.close()
            raise StopIteration       


    def _load_file(self, schema: str, table: str):
        schema, table = schema.lower(), table.lower()
        data_path = os.path.join(DB_DIR, schema, table + ".csv")
        # print(f"Loading data from {data_path}")
        try:
            return open(data_path, "r", encoding="utf-8")
        except FileNotFoundError:
            # print(self.table_name)
            raise FileNotFoundError(f"Table {self.table_name} not found.")
        except Exception as e:
            raise Exception(f"Error loading table {self.table_name}: {e}")
        
    def _check_header(self) -> None:
        header = next(self._reader)
        if len(header) != len(self._columns):
            raise ValueError(f"Header length does not match column length in {self.schema}/{self.table_name}.")
        if any(col.lower() != header[i].lower() for i, col in enumerate(self._columns)):
            raise ValueError(f"Header names do not match column names in {self.schema}/{self.table_name}.")

    def __del__(self):
        self.close()

    def __repr__(self):
        result = f"Table: {self.table_name}\n"
        columns = [f"\n\t{col} ({typ})" for col, typ in zip(self._columns, self._column_types)]
        result += f"Columns: {''.join(columns)}\n"
        
        col_widths = [max(len(str(cell)) for cell in [col] + [row[i] for row in self._data]) for i, col in enumerate(self._columns)]

        header = [h.ljust(width) for h, width in zip(self._columns, col_widths)]
        result += " | ".join(header) + "\n"
        result += "-" * (sum(col_widths) + 3 * (len(header) - 1)) + "\n"

        for row in self._cache:
            row_str = [str(cell).ljust(width) for cell, width in zip(row, col_widths)]
            result += " | ".join(row_str) + "\n"

        return result
    
    def close(self) -> None:
        if hasattr(self, "_file") and self._file:
            self._file.close()
    
    def to_json(self, limit: int = None):
        if not limit:
            limit = self.batch_size

        tmp_file = self._load_file(schema=self.schema, table=self.table_name)
        tmp_reader = csv.reader(tmp_file)
        next(tmp_reader)  # Skip the header

        data = []
        for i, row in enumerate(tmp_reader):
            if i >= limit:
                break
            if len(row) != len(self._columns):
                raise ValueError(f"Row length does not match column length in {self.schema}/{self.table_name}.")
            data.append(row)

        tmp_file.close()

        result = {
            "table_name": self.table_name,
            "columns": self._columns,
            "column_types": self._column_types,
            "data": data
        }
        return json.dumps(result, indent=4)

    @property
    def cache(self):
        return self._cache

    @property
    def columns(self):
        return self._columns

    @property
    def column_types(self):
        return self._column_types
