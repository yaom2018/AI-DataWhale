import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

class User(BaseModel):
    username: str
    full_name: str | None = None
@app.post("/items/")
async def read_item(item: Item, user: User):
    return {"name":item.name, "price":item.price, "user": user}

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)