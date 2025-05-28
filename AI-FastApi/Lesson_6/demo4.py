import uvicorn
from typing import Annotated
from fastapi import Body, FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

body_examples = {
    "name": "细胞生物学",
    "description": "考研书籍",
    "price": 35.8,
    "tax": 0.6,
}


@app.post("/items/{item_id}")
async def update_item(item_id: int, item: Annotated[Item, Body(embed=True,example=body_examples)]):
    results = {"item_id": item_id, "item": item}
    return results

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)