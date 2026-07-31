FROM python:3.10
ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /app

# 1. GRAPHICS ENGINE OVERRIDE: Prevent OpenCV container hardware driver dependency crashes
RUN pip install --no-cache-dir streamlit requests Pillow numpy ultralytics && \
    pip install --no-cache-dir --force-reinstall opencv-python-headless

# Copy frontend app and weights assets directly into workspace context
COPY app.py .
COPY final_production_model_50_epochs.pt .

EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
