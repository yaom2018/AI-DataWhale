# FastAPI 框架

## 第01课-路径参数
关于异步编程
async await 关键字

交互式文档
http://127.0.0.1:8000/docs

第一个接口
http://127.0.0.1:8000

### 枚举值使用
```python
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

app = FastAPI()

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
```

### 路径参数定义
```python
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}
```

## 第02课-查询参数
1. 默认值

2. 必须值
如果你不想添加一个特定的值，而只是想使该参数成为可选的，则将默认值设置为 None。
但当你想让一个查询参数成为必需的，不声明任何默认值就可以

注意：在参数入口时，
async def read_user_item(item_id: int = 1, needy: str): 
这样是错误的，必须在参数后面声明默认值，才能让参数变为可选参数。
或者 async def read_user_item(item_id: int = 1, *, needy: str):  # 正确！

3. 可选参数
@app.get("/items/{item_id}")
async def read_item(item_id: str, q: Union[str, None] = None):

4. 混合参数
async def read_user_item(user_id: int, item_id: str, q: Union[str, None] = None, short: bool = False):

## 第03课-路径参数校验
async def read_items(
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=5)]
):

## 第04课-查询参数校验
更多校验 和 正则表达式
async def read_items(q: str | None = Query(default=None, min_length=3, max_length=5, pattern="^test.?$")):

声明为必需参数
async def read_items(q: str = Query(min_length=3, max_length=5, pattern="^test.?$")):
使用省略号(...)声明必需参数
async def read_items(q: str = Query(default=..., min_length=3)):

## 第05课-请求体参数

查询参数
    async def read_item(item_id: int):

请求体参数
    async def read_item(item_id: Annotated[int, Body()]):

多个请求体参数
    async def read_item(item_id: Annotated[int, Body()], name: Annotated[str, Body()]):
    请求体参数可以在post/put/patch/delete等方法中使用，
    但在get方法中使用时，会被忽略。

单个Pydantic 模型请求体参数
    class Item(BaseModel):
        name: str
        description: str | None = None
        price: float
        tax: float | None = None

    @app.post("/items/")
    async def create_item(item: Item):

混合使用 Path、Query 和请求体参数
    async def read_item(name: str, age: int, item_id: Annotated[int, Body()]):

多个Pydantic 模型请求体参数
    class Item(BaseModel):
        name: str
        description: str | None = None
        price: float
        tax: float | None = None

    class User(BaseModel):
        username: str
        full_name: str | None = None
    @app.post("/items/")
    async def read_item(item: Item, user: User):

嵌入单个请求体参数
    class Item(BaseModel):
        name: str
        description: str | None = None
        price: float
        tax: float | None = None
    @app.post("/items/")
    async def read_item(item: Item = Body(embed=True)):

## 第06课-额外参数信息
使用 Pydantic 的 Field 在 Pydantic 模型内部声明校验和元数据
就是对定义的输入每一个字段的校验和元数据信息的描述。
```python
class Item(BaseModel):
    name: str
    description: str | None = Field(
        default=None, title="The description of the item", max_length=300
    )
    price: float = Field(gt=0, description="The price must be greater than zero")
    tax: float | None = None

@app.post("/items/{item_id}")
async def update_item(item_id: int, item: Annotated[Item, Body(embed=True)]):
```

模式-例子
```python
class Item(BaseModel):
    name: str
    description: str | None = Field(
        default=None, title="The description of the item", max_length=300
    )
    price: float = Field(gt=0, description="The price must be greater than zero")
    tax: float | None = None
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                }
            ]
        }
    }
```

Field 的附加参数
```python
class Item(BaseModel):
    name: str = Field(examples=["Foo"])
    description: str | None = Field(default=None, examples=["A very nice Item"])
    price: float = Field(examples=[35.4])
    tax: float | None = Field(default=None, examples=[3.2])
```

Body 额外参数
```python
body_examples = {
    "name": "细胞生物学",
    "description": "考研书籍",
    "price": 35.8,
    "tax": 0.6,
}


@app.post("/items/{item_id}")
async def update_item(item_id: int, item: Annotated[Item, Body(embed=True,example=body_examples)]):
```

额外数据类型
```python

```

## 第07课-嵌套模型




















[参考课程](https://www.datawhale.cn/learn/content/164/3837)