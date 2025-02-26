FROM python:3.9

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8001

ENV JWT_SERVER="127.0.0.1:8002"
ENV MYSQL_HOST=mysql
ENV MYSQL_USER=root
ENV MYSQL_PASSWORD=root
ENV MYSQL_DB=mydb
ENV MYSQL_PORT=3306

CMD ["python", "user_management.py"]
