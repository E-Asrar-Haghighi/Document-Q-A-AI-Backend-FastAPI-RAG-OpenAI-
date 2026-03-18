# ----------------------------------------------------
# Base image
# ----------------------------------------------------
# Use a lightweight Python image for smaller builds.
FROM python:3.11-slim

# ----------------------------------------------------
# Working directory inside the container
# ----------------------------------------------------
WORKDIR /app

# ----------------------------------------------------
# Copy dependency file first for better Docker caching
# ----------------------------------------------------
COPY requirements.txt .

# ----------------------------------------------------
# Install Python dependencies
# ----------------------------------------------------
RUN pip install --no-cache-dir -r requirements.txt

# ----------------------------------------------------
# Copy the application code into the container
# ----------------------------------------------------
COPY app ./app

# ----------------------------------------------------
# Expose the FastAPI port
# ----------------------------------------------------
EXPOSE 8000

# ----------------------------------------------------
# Start the FastAPI app
# ----------------------------------------------------
# 0.0.0.0 is required so the app is reachable outside the container.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]