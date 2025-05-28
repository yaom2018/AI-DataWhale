import uvicorn
from fastapi import FastAPI
from typing import Union

app = FastAPI()

#多种入参格式
@app.get("/items/{item_id}")
async def read_item(item_id: str, needy: str, skip: int = 0, q: Union[str, None] = None):
    if q == None:
        return {"item_id": item_id, "needy": needy, "skip": skip}
    item = {"item_id": item_id, "needy": needy, "skip": skip, "q": q}
    return item

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)