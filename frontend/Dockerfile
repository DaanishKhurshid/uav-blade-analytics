FROM python:3.10-slim
ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /app

# Install package dependencies required by the frontend interface
RUN pip install --no-cache-dir streamlit requests Pillow opencv-python-headless numpy

# Copy only the frontend interface script
COPY app.py .

EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
