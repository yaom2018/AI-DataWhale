import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}")
async def read_user_item(item_id: int, needy: str):
    return {"item_id": item_id, "needy": needy}

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)