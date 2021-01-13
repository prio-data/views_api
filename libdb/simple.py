from fastapi import FastAPI, APIRouter, Query
from typing import Optional, List

app = FastAPI()
@app.get("/")
async def get_root():
    return 1

@app.get("/{run}")
async def get_run(run: List[int]):
    return run

