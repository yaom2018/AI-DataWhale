import uvicorn
from fastapi import FastAPI,Body
from pydantic import BaseModel
app = FastAPI()
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
@app.post("/items/")
async def read_item(item: Item = Body(embed=True)):
    return {"name":item.name, "price":item.price}

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)