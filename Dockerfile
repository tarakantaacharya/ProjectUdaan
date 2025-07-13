FROM python:3.9-slim

WORKDIR /app

# Create directory for database and ensure proper permissions
RUN mkdir -p /app/data && chmod 755 /app/data

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Ensure the app directory has proper permissions
RUN chmod -R 755 /app

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
