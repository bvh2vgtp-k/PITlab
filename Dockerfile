FROM python:3.14

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/

EXPOSE 8000

WORKDIR /app/src

CMD ["python", "main.py"]
