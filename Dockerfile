FROM python:3.11-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制源码
COPY app.py .
COPY templates/ templates/
COPY static/ static/

# 创建数据目录
RUN mkdir -p /app/data

# 启动
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7000"]
