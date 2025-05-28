import uvicorn
from fastapi import FastAPI
from typing import Union

app = FastAPI()

# 可选查询参数
@app.get("/items/{item_id}")
async def read_item(item_id: str, q: Union[str, None] = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}

# 路径参数和可选查询参数
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)