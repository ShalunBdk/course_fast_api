from typing import Annotated

from fastapi import Depends, Query
from pydantic import BaseModel

class PaginationParams(BaseModel):
    page: Annotated[int  | None, Query(1, ge=1,description="Страница")]
    per_page: Annotated[int  | None, Query(None, ge=1, lt=100, description="Кол-во отелей на странице")]

PaginationDep = Annotated[PaginationParams, Depends()]