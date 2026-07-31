FROM python:3.10
ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /app

# 1. RUNTIME DEPENDENCIES: Force headless OpenCV to bypass Linux libGL hardware errors
RUN pip install --no-cache-dir opencv-python-headless fastapi uvicorn ultralytics Pillow python-multipart

# Copy only the backend code and weights
COPY main.py .
COPY final_production_model_50_epochs.pt .

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
