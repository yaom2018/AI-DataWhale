import uvicorn
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image
import io
import torch
from torchvision import transforms
import torchvision.models as models
from PIL import Image, ImageFilter, ImageEnhance
import numpy as np
import base64
import cv2
from openai import OpenAI

# 环境变量加载相关
from dotenv import load_dotenv # 导入环境变量加载工具
import os # 用于获取环境变量值


# Load environment variables from .env file
load_dotenv()
app = FastAPI()


# 设置DeepSeek API密钥
API_KEY = os.getenv("API_KEY")
# 设置DeepSeek API基础URL
BASE_URL = os.getenv("BASE_URL")
# 设置DeepSeek API模型名称
MODEL_NAME = os.getenv("MODEL_NAME")

# 初始化OpenAI客户端
client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL,
)


# 加载预训练模型
model = models.detection.fasterrcnn_resnet50_fpn(pretrained=True)
model.eval()

# 定义图片预处理
transform = transforms.Compose([
    transforms.ToTensor(),
])

# 在transform定义后添加预处理函数
def preprocess_image(image):
    # 转换为OpenCV格式
    img = np.array(image)
    
    # 去噪
    img = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)
    
    # 纠偏 (自动检测和矫正倾斜)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength=100, maxLineGap=10)
    
    if lines is not None:
        angles = []
        for line in lines:
            x1, y1, x2, y2 = line[0]
            angles.append(np.arctan2(y2 - y1, x2 - x1))
        
        median_angle = np.median(angles) * 180 / np.pi
        if abs(median_angle) > 1:  # 只在校正角度大于1度时执行
            (h, w) = img.shape[:2]
            center = (w // 2, h // 2)
            M = cv2.getRotationMatrix2D(center, median_angle, 1.0)
            img = cv2.warpAffine(img, M, (w, h), borderMode=cv2.BORDER_REPLICATE)
    
    # 增强对比度和锐度
    img = Image.fromarray(img)
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.5)
    enhancer = ImageEnhance.Sharpness(img)
    img = enhancer.enhance(2.0)
    
    return img

@app.post("/recognize/")
async def recognize_objects(file: UploadFile = File(...)):
    # 读取上传的图片
    image_data = await file.read()
    image = Image.open(io.BytesIO(image_data)).convert("RGB")
    
    # 预处理图片
    image = preprocess_image(image)
    
    # 将图片保存为临时文件
    temp_img_path = "temp_image.jpg"
    image.save(temp_img_path)
    
    # 使用OpenAI API进行识别
    with open(temp_img_path, "rb") as img_file:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "描述这张图片中的主要内容，请用小朋友能听懂的简答话回答。"},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64.b64encode(img_file.read()).decode('utf-8')}"}}
                    ]
                }
            ],
            max_tokens=100
        )
    
    # 获取并处理响应
    description = response.choices[0].message.content
    response_text = f"你画了{description}，是吗？" if description else "我无法确定你画了什么"
    
    return JSONResponse(content={"description": response_text})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

