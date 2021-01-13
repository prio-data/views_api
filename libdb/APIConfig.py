from fastapi import FastAPI, APIRouter, Query
from dataclasses import dataclass

@dataclass
class Paging:
    pagesize = Query(default=1000, ge=0, le=10000)
    page = Query(default=1, ge=1)