import uvicorn
from fastapi import FastAPI

app = FastAPI()

fake_item_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

# 默认值设定
@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_item_db[skip : skip + limit]

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)