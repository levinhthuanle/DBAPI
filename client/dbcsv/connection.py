from typing import Optional, List, Any
from dbapi2.utils import validate_dsn_url, login, query, validate_token
from dbapi2.exception import (
    InternalError, NotSupportedError, OperationalError, ProgrammingError,
    InterfaceError, AuthenticationError
)


class Connection:
    def __init__(self, token: str):
        self.token = token
        self._url = None
        self._is_online = True
        self._schema = None

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, url):
        self._url = url

    @property
    def is_online(self):
        return self._is_online

    @property
    def schema(self):
        return self._schema

    @schema.setter
    def schema(self, schema):
        self._schema = schema

    def cursor(self) -> "Cursor":
        if not self._is_online:
            raise InterfaceError("Cannot create a cursor from a closed connection")
        return Cursor(self)

    def rollback(self):
        if not self._is_online:
            raise InterfaceError("Connection is closed.")
        raise NotSupportedError("rollback() is currently not supported")

    def commit(self):
        if not self._is_online:
            raise InterfaceError("Connection is closed.")
        pass  # Optional: auto-commit behavior

    def close(self):
        if not self._is_online:
            raise InterfaceError("Connection is already closed")
        self._is_online = False


class Cursor:
    def __init__(self, connection: Connection):
        self.arraysize = 1000000
        self._connection = connection
        self._description = None
        self._rowcount = -1
        self._is_open = True
        self._result_iter = None

    @property
    def description(self):
        return self._description

    @property
    def is_open(self):
        return self._is_open

    def close(self):
        if not self._connection.is_online:
            raise InterfaceError("Cannot close cursor from a closed connection")
        if not self._is_open:
            raise InterfaceError("Cursor is already closed")
        self._is_open = False
        self._result_iter = None

    def execute(self, q: str, parameters=None) -> None:
        if not self._connection.is_online:
            raise InterfaceError("Cannot execute on a closed connection")
        if not self._is_open:
            raise InterfaceError("Cannot execute on a closed cursor")

        try:
            new_token = validate_token(self._connection.url, self._connection.token)
        except Exception as e:
            raise AuthenticationError("Token validation failed") from e

        if new_token is not None:
            self._connection.token = new_token

        try:
            self._result_iter = query(
                self._connection.url,
                self._connection.token,
                self._connection.schema,
                q
            )
        except Exception as e:
            raise ProgrammingError("Query execution failed") from e

    def _ensure_executed(self):
        if self._result_iter is None:
            raise ProgrammingError("No query executed before fetching results")

    def fetchone(self):
        self._ensure_executed()
        if not self._connection.is_online:
            raise InterfaceError("Cannot fetch from a closed connection")
        if not self._is_open:
            raise InterfaceError("Cannot fetch from a closed cursor")
        try:
            return tuple(next(self._result_iter))
        except StopIteration:
            return None

    def fetchmany(self, size=None):
        self._ensure_executed()
        if not self._connection.is_online:
            raise InterfaceError("Cannot fetch from a closed connection")
        if not self._is_open:
            raise InterfaceError("Cannot fetch from a closed cursor")
        size = size or self.arraysize
        result = []
        try:
            for _ in range(size):
                result.append(tuple(next(self._result_iter)))
        except StopIteration:
            pass
        return result

    def fetchall(self):
        self._ensure_executed()
        if not self._connection.is_online:
            raise InterfaceError("Cannot fetch from a closed connection")
        if not self._is_open:
            raise InterfaceError("Cannot fetch from a closed cursor")
        return self.fetchmany()

    def setinputsizes(self, sizes: List[Any]):
        raise NotSupportedError(
            "setinputsizes() is not supported. Implemented only for DBAPI2 compatibility."
        )

    def setoutputsize(self, sizes: List[Any], column=None):
        raise NotSupportedError(
            "setoutputsize() is not supported. Implemented only for DBAPI2 compatibility."
        )


def connect(
    dsn: str,
    user: Optional[str],
    password: Optional[str],
) -> Connection:
    schema, url = validate_dsn_url(dsn)
    try:
        token = login(url, user, password)
    except Exception as e:
        raise AuthenticationError("Login failed. Check credentials or server availability.") from e

    conn = Connection(token=token)
    conn.schema = schema
    conn.url = url
    return conn