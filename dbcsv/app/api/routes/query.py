from typing import Annotated

from fastapi import APIRouter, Depends

from dbcsv.app.api.schemas.auth import User
from dbcsv.app.api.schemas.sql_request import SQLRequest
from dbcsv.app.core.database_engine import DatabaseEngine, get_engine
from dbcsv.app.dependencies import current_user_dependency
from fastapi.responses import StreamingResponse
import json

router = APIRouter(prefix="/query", tags=["Query"])


# @router.post("/sql/stream")
# def query_by_sql_stream(
#     sql_request: SQLRequest,
#     current_user: Annotated[User, current_user_dependency],
#     database_engine: Annotated[DatabaseEngine, Depends(get_engine)],
# ):
#     result_iterator = database_engine.execute(
#         sql_request.sql_statement, sql_request.schema
#     )

#     def row_stream():
#         yield "[\n"
#         first = True
#         for row in result_iterator:
#             if not first:
#                 yield ",\n"
#             else:
#                 first = False
#             yield json.dumps(row)
#         yield "\n]"

#     return StreamingResponse(row_stream(), media_type="application/json")


@router.post("/sql")
def query_by_sql(
    sql_request: SQLRequest,
    current_user: Annotated[User, current_user_dependency],
    database_engine: Annotated[DatabaseEngine, Depends(get_engine)],
):
    result = database_engine.execute(sql_request.sql_statement, sql_request.schema)
    
    return list(result)
