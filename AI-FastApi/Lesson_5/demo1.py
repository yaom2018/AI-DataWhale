import uvicorn
from fastapi import FastAPI, Body
from typing import Annotated

app = FastAPI()

# 查询参数
@app.post("/items/")
async def read_item(item_id: int):
    return {"item_id": item_id}

# 请求体参数
@app.put("/itemsBody/")
async def read_item(item_id: Annotated[int, Body()]):
    return {"item_id": item_id}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)