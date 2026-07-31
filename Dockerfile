FROM python:3.10
ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /app

# 1. CACHED LIBRARY LAYER: Pull foundational tools from your hard drive cache
RUN pip install --no-cache-dir opencv-python-headless fastapi uvicorn ultralytics Pillow python-multipart requests streamlit

# 2. FIXED VERSION LAYER: Force upgrade the package to patch the Streamlit Unpack bug
RUN pip install --no-cache-dir --upgrade typing-extensions

# Mirror the clean folders into Docker's virtual machine space
COPY backend/ /app/backend/
COPY frontend/ /app/frontend/

EXPOSE 8501
CMD ["streamlit", "run", "frontend/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
