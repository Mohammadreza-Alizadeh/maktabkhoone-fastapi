from typing import Annotated
from fastapi import FastAPI, Path, status
from fastapi.responses import JSONResponse


EXPENSES_LIST: list[dict] = [
    {"id": 1, "description": "coffe", "amount": 80.5},
    {"id": 2, "description": "lunch", "amount": 180},
    {"id": 3, "description": "snap", "amount": 100.7},
]

last_used_id: int = 3

app = FastAPI()


@app.get("/expenses")
def get_expenses_list():
    return JSONResponse(content=EXPENSES_LIST, status_code=status.HTTP_200_OK)


@app.get("/expenses/{id}")
def get_expense(
    expense_id: Annotated[
        int,
        Path(
            gt=0,
            title="Expense id to retrive",
            desc="i use this id to find desired expense",
            alias="id",
        ),
    ],
):
    for item in EXPENSES_LIST:
        if item["id"] == expense_id:
            return JSONResponse(content=item, status_code=status.HTTP_200_OK)
    return JSONResponse(
        content={"detail": "not found"}, status_code=status.HTTP_404_NOT_FOUND
    )
