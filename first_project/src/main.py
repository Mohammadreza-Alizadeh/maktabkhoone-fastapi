from typing import Annotated
from fastapi import Body, FastAPI, Path, status
from fastapi.responses import JSONResponse


EXPENSES_LIST: list[dict] = [
    {"id": 1, "description": "coffe", "amount": 80.5},
    {"id": 2, "description": "lunch", "amount": 180},
    {"id": 3, "description": "snap", "amount": 100.7},
]


def generate_new_id():
    last_expense_pushed = EXPENSES_LIST[-1]
    new_id = last_expense_pushed["id"] + 1
    return new_id


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


@app.post("/expenses")
def add_expense(
    description: Annotated[
        str, Body(title="Expence Description", description="What this expense is for ?")
    ],
    amount: Annotated[
        float,
        Body(
            gt=0, title="Expence Amount", description="How much moneu did you spend ?"
        ),
    ],
):
    new_expense = {
        "id": generate_new_id(),
        "description": description,
        "amount": amount,
    }
    EXPENSES_LIST.append(new_expense)

    return JSONResponse(content=new_expense, status_code=status.HTTP_201_CREATED)


@app.delete("/expenses/{id}")
def delete_expense(
    expense_id: Annotated[
        int,
        Path(
            gt=0,
            title="Expense id to delete",
            desc="i use this id to find desired expense and delete it",
            alias="id",
        ),
    ],
):
    for item in EXPENSES_LIST:
        if item["id"] == expense_id:
            EXPENSES_LIST.remove(item)
            return JSONResponse(
                content={"detail": "deleted succesfully"},
                status_code=status.HTTP_202_ACCEPTED,
            )
    return JSONResponse(
        content={"detail": "not found"}, status_code=status.HTTP_404_NOT_FOUND
    )


@app.put("/expenses/{id}")
def delete_expense(
    expense_id: Annotated[
        int,
        Path(
            gt=0,
            title="Expense id to update",
            desc="i use this id to find desired expense and update it",
            alias="id",
        ),
    ],
    new_description: Annotated[
        str,
        Body(
            title="New Description",
            desc="new description to update",
        ),
    ],
    new_amount: Annotated[
        float,
        Body(
            gt=0,
            title="New Amount",
            desc="new amount to update",
        ),
    ],
):
    for item in EXPENSES_LIST:
        if item["id"] == expense_id:
            item["description"] = new_description
            item["amount"] = new_amount

            return JSONResponse(
                content={"detail": "updated succesfully"},
                status_code=status.HTTP_200_OK,
            )
    return JSONResponse(
        content={"detail": "not found"}, status_code=status.HTTP_404_NOT_FOUND
    )
