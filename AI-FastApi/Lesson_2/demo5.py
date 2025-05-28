import uvicorn
from fastapi import FastAPI
from typing import Union

app = FastAPI()

@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(user_id: int, item_id: str, q: Union[str, None] = None, short: bool = False):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}  
        )    
    return item

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)    



