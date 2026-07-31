FROM python:3.10-slim
ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /app

# 1. RUNTIME DEPENDENCIES: Install standard framework libraries
RUN pip install --no-cache-dir streamlit requests Pillow opencv-python-headless numpy ultralytics

# Copy your frontend dashboard script
COPY app.py .

# 2. LOCAL ASSET COPY: Copy the weights directly from the local frontend folder context
COPY final_production_model_50_epochs.pt .

EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
