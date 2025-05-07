# Use official Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy dependencies
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire project
COPY . .

# Expose the port FastAPI runs on
EXPOSE 8000

# Command to run the FastAPI app
CMD ["uvicorn", "app.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
