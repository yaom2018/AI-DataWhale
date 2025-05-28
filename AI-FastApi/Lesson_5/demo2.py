import uvicorn
from fastapi import Body, FastAPI
from typing import Annotated
app = FastAPI()
@app.post("/items/")
async def read_item(item_id: Annotated[int, Body()], name: Annotated[str, Body()]):
    return {"item_id": item_id, "name": name}

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)