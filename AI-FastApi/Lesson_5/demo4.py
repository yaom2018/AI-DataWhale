import uvicorn
from fastapi import FastAPI, Body
from typing import Annotated

app = FastAPI()

@app.post("/items/{name}")
async def read_item(name: str, age: int, item_id: Annotated[int, Body()]):
    return {"name": name, "age": age, "item_id": item_id}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)