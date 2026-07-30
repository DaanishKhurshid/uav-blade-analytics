FROM python:3.10
ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /app

RUN pip install --no-cache-dir opencv-python-headless fastapi uvicorn ultralytics Pillow python-multipart requests streamlit

# Mirror the clean folders into Docker's virtual machine space
COPY backend/ /app/backend/
COPY frontend/ /app/frontend/

EXPOSE 8501
CMD ["streamlit", "run", "frontend/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
