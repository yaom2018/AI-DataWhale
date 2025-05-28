# 用于发送http请求
import httpx
# 用于创建MCP服务
from mcp.server.fastmcp import FastMCP
import pymysql
from dotenv import load_dotenv # 导入环境变量加载工具
import os # 用于获取环境变量值
from typing import Any

mcp = FastMCP("mcpmysql")

load_dotenv() 

# 核心的MYSQL查询服务，查询工作流的名字获取数据
async def make_workflow_request(flowName: str) -> dict[str, Any] | None:
    """
       获取到输入，进行check
       查询数据库模糊查询
       返回查询数据
    """
    if not flowName:
        print("输入为空，请确认输入字段") 
        return None;

    print("查询mysql开始")
   
    result = query_workflow_by_flowName(flowName)

    print(result)
    return result
    

def query_workflow_by_flowName(flowName: str):

    # 数据库连接参数请根据实际情况修改
    connection = pymysql.connect(
        host=os.getenv("MYSQL_HOST"),
        port=int(os.getenv("MYSQL_PORT", 3306)), 
        user=os.getenv("MYSQL_NAME"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE"),
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor 
    )
    print("数据库连接成功！")

    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM workflow WHERE flow_name LIKE %s LIMIT 1"
            like_pattern = f"%{flowName}%"
            cursor.execute(sql, (like_pattern,))
            results = cursor.fetchone()
            print(f"数据库返回值：{results}")
            return results
        
    except Exception as e:
        print(f"数据库查询出错：{e}")
        return None
    finally:
        connection.close()

@mcp.tool()
async def get_mysql_flow_data(flowName: str) -> str:
    """
    获取指定流程的具体信息，如果用户使用中文询问流程的具体信息，你就获取询问中的流程信息作为输入。

    Args:
        flowName: 流程名字(如：物品调拨，采购流程)
    
    Returns:
        str: 格式化的流程具体信息
    """

    # 调用Mysql请求
    data = await make_workflow_request(flowName)
    if not data:
        return "没有获取到Mysql中的数据！"
    
    flowid = data.get("flow_id","未知")
    communityid = data.get("community_id","未知")

    # 构建格式化的天气信息字符串
    return f"""
    流程名字: {flowName}
    流程号: {flowid}
    小区号: {communityid}
    """    


def query_product_by_prodName(prodName: str):

    # 数据库连接参数请根据实际情况修改
    connection = pymysql.connect(
        host=os.getenv("MYSQL_HOST"),
        port=int(os.getenv("MYSQL_PORT", 3306)), 
        user=os.getenv("MYSQL_NAME"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE"),
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor 
    )
    print("数据库连接成功！")

    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM market_goods_item WHERE prod_name LIKE %s LIMIT 1"
            like_pattern = f"%{prodName}%"
            cursor.execute(sql, (like_pattern,))
            results = cursor.fetchone()
            print(f"数据库返回值：{results}")
            return results
        
    except Exception as e:
        print(f"数据库查询出错：{e}")
        return None
    finally:
        connection.close()

# 核心的MYSQL查询服务，查询工作流的名字获取数据
async def make_product_request(prodName: str) -> dict[str, Any] | None:
    """
       获取到输入，进行check
       查询数据库模糊查询
       返回查询数据
    """
    if not prodName:
        print("输入为空，请确认输入字段") 
        return None;

    print("查询mysql开始")
   
    result = query_product_by_prodName(prodName)

    print(result)
    return result
    

@mcp.tool()
async def get_mysql_product_data(prodName: str) -> str:
    """
    获取指定产品的具体信息，如果用户使用中文询问产品的具体信息，你就获取询问中关于产品的信息作为输入。

    Args:
        prodName: 产品名称(如：苹果电脑，小米手机，华为手机)
    
    Returns:
        str: 格式化的产品具体信息
    """

    # 调用Mysql请求
    data = await make_product_request(prodName)
    if not data:
        return "没有获取到Mysql中的数据！"
    
    prodDesc = data.get("prod_desc","未知")
    picUrl = data.get("pic_url","未知")

    # 构建格式化的天气信息字符串
    return f"""
    品牌: {prodName}
    型号: {prodDesc}
    展示链接: {picUrl}
    """    



if __name__ == "__main__":
    mcp.run(transport='stdio')
