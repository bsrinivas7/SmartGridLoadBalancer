FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt  # Add this line
COPY test.py .
CMD ["python", "test.py"]
