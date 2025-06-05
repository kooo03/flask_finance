FROM python:3.11-slim

WORKDIR /app

# 正确安装 netcat（使用 netcat-openbsd 实现）
RUN apt-get update && apt-get install -y netcat-openbsd

COPY . /app
RUN chmod +x /app/wait-for-db.sh


RUN pip install --no-cache-dir -r requirements.txt

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

EXPOSE 5000

CMD ["sh", "-c", "python init_db.py && python app.py"]

