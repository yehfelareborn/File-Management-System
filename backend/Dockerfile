# 使用 Python 官方鏡像作為基礎
FROM python:3.9-slim

# 設置工作目錄
WORKDIR /app

# 安裝依賴
COPY requirements.txt .
RUN pip install -r requirements.txt

# 複製應用代碼
COPY . .

# 暴露 Flask 端口
EXPOSE 5000

# 啟動 Flask 應用
CMD ["python", "app.py"]
