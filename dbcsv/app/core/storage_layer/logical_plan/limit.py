from typing import List, Any, Iterator
from dbcsv.app.core.storage_layer.logical_plan.logical_plan import LogicalPlan

class Limit(LogicalPlan):
    def __init__(self, child: LogicalPlan, limit: int):
        self.child = child
        self.limit = limit

    def execute(self) -> Iterator[List[Any]]:
        return (row for i, row in enumerate(self.child.execute()) if i < self.limit)

    @property
    def columns(self) -> List[str]:
        return self.child.columns

    @property
    def column_types(self) -> List[str]:
        return self.child.column_types

    def __repr__(self):
        return f"{self.__class__.__name__}(limit={self.limit}, child={self.child})"