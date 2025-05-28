import uvicorn
from typing import Annotated, Union
from fastapi import FastAPI, Path

app = FastAPI()

#路径参数校验
@app.get("/items/{item_id}")
async def read_items(
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=5, le=10)]
):
    results = { "item_id": item_id}
    return results

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)