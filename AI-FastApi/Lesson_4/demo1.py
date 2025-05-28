import uvicorn
from fastapi import FastAPI, Query
app = FastAPI()
@app.get("/items/")
async def read_items(q: str | None = Query(default=None, max_length=5, min_length=2, regex="^[a-zA-Z0-9_]+$")):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)