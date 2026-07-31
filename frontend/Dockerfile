FROM python:3.10-slim
ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /app

# 1. FIXED DEPENDENCY LAYER: Added ultralytics to satisfy the python script import
RUN pip install --no-cache-dir streamlit requests Pillow opencv-python-headless numpy ultralytics

# Copy your frontend dashboard script
COPY app.py .

# Copy your model weights file directly into the frontend container root space for the fallback path
COPY final_production_model_50_epochs.pt .

EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
