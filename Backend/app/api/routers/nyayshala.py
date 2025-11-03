from __future__ import annotations
from fastapi import APIRouter, Query
from datetime import date, datetime
from typing import Optional
from app.services.nyayshala_generator import generate_for_day, read_for_day, FIELDS

router = APIRouter(prefix="/nyayshala", tags=["nyayshala"])


@router.get("/daily")
def daily(field: Optional[str] = Query(None)):
    today = date.today()
    data = read_for_day(today)
    if data is None:
        items = generate_for_day(today)
        data = {"date": today.isoformat(), "items": items}
    if field and field in FIELDS:
        data = {**data, "items": [i for i in data["items"] if i["field"] == field]}
    return data


@router.get("/archive")
def archive(date_str: str = Query(..., description="YYYY-MM-DD")):
    d = datetime.strptime(date_str, "%Y-%m-%d").date()
    data = read_for_day(d)
    if data is None:
        return {"date": d.isoformat(), "items": []}
    return data


@router.post("/generate")
def generate():
    today = date.today()
    items = generate_for_day(today)
    return {"date": today.isoformat(), "items": items}
