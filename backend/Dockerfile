FROM python:3.10
ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /app

# 1. RUNTIME DEPENDENCIES: Install ultralytics first, then explicitly overwrite with headless OpenCV
RUN pip install --no-cache-dir fastapi uvicorn ultralytics Pillow python-multipart && \
    pip install --no-cache-dir --force-reinstall opencv-python-headless

# Copy only the backend code and weights
COPY main.py .
COPY final_production_model_50_epochs.pt .

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
