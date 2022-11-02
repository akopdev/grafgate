from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple, Union
from pydantic import BaseModel, Field


class Column(BaseModel):
    text: str
    type: Optional[str] = Field(default="string")  # should be enum


class Table(BaseModel):
    type: Optional[str] = Field(default="table")
    columns: List[Column]
    rows: List[List[Any]] = Field(default=list)


class Timeseries(BaseModel):
    target: str
    datapoints: List[Union[List, Tuple]]


class Target(BaseModel):
    target: str
    payload: Dict[str, Any] = Field(default=dict)


class Range(BaseModel):
    start: datetime = Field(alias="from")
    end: datetime = Field(alias="to")


class Payload(BaseModel):
    targets: List[Target]
    range: Range
