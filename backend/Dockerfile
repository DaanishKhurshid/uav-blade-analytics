FROM python:3.10-slim
ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /app

# Install package dependencies required by the backend
RUN pip install --no-cache-dir fastapi uvicorn ultralytics Pillow python-multipart

# Copy only the backend code and weights
COPY main.py .
COPY final_production_model_50_epochs.pt .

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
