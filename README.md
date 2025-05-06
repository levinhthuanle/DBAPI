"""
DBCsv Database API (PEP 249 Compliant)

Supported Features:
--------------------
- **Connection Management**:
  - Establish connections to the database using `connect()`.
  - Close connections gracefully.

- **Cursor Operations**:
  - Create cursors for executing SQL queries.
  - Close cursors after use.

- **SQL Execution**:
  - Execute SQL queries using `execute()`.
  - Fetch results using `fetchone()`, `fetchmany(size)`, and `fetchall()`.

- **Transaction Management**:
   `commit(), rollback()`: Raises `NotSupportedError` as transactions are not supported.

- **Error Handling**:
  - Standard PEP 249 exceptions are implemented:
    - `InterfaceError`, `DatabaseError`, `DataError`, `OperationalError`,
      `IntegrityError`, `InternalError`, `ProgrammingError`, `NotSupportedError`,
      `AuthenticationError`.

Supported API:
--------------
1. `connect(dsn: str, user: str, password: str) -> Connection`:
   - Establishes a connection to the database.
   - Parameters:
     - `dsn`: Data Source Name (e.g., "https://localhost:8000/schema").
     - `user`: Username for authentication.
     - `password`: Password for authentication.
   - Returns: A `Connection` object.

2. `Connection`:
   - `cursor() -> Cursor`: Creates a new cursor object.
   - `close() -> None`: Closes the connection.
   - `commit(), rollback()`: Raises `NotSupportedError` as transactions are not supported.

3. `Cursor`:
   - `execute(query: str) -> None`:
     Executes a SQL query.
   - `fetchone() -> Union[List[Any], None]`: Fetches the next row of the result set.
   - `fetchmany(size: Optional[int] = None) -> List[List[Any]]`: Fetches the next `size` rows.
   - `fetchall() -> List[List[Any]]`: Fetches all remaining rows.
   - `close() -> None`: Closes the cursor.
   - `rowcount`: Returns the number of rows fetched so far.
   - `description`: Metadata about the result set (not implemented).

4. Exceptions:
   - `Error`: Base class for all exceptions.
   - `InterfaceError`, `DatabaseError`, `DataError`, `OperationalError`,
     `IntegrityError`, `InternalError`, `ProgrammingError`, `NotSupportedError`,
     `AuthenticationError`: Throw when token has expired
"""
