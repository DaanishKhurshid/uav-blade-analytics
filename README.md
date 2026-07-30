# Autonomous UAV Wind Turbine Blade Inspection System

An application that processes high-resolution aerial drone imagery to localize structural turbine defects.

## Architectural Topology
The application is built using a decoupled split-tier infrastructure to ensure universal portability, scalability, and edge-computing optimization:

- Frontend Interface (frontend/app.py): An interactive Streamlit dashboard configured to handle automated asset file uploads, coordinate map extraction, and automated report rendering.
- Backend AI Engine (backend/main.py): A high-performance FastAPI listener node that houses the deep-learning weights and executes the computer vision inference pipeline.

## Machine Learning Framework and Training Pipeline
- Core Architecture: YOLOv8 Object Detection Network.
- Training Environment: Google Colab Enterprise Cloud GPU Accelerators.
- Hyperparameters: Trained for 50 Epochs utilizing an input grid scale of 1024x1024 pixels to preserve high-frequency edge features.
- Metric Tracking: Integrated logging via Weights and Biases (W&B) to monitor bounding box regression losses and class accuracy fluctuations over the 50 epochs.
- Class Labels Configured: Corrosion, Crack, Craze, Hidden Craze, Surface Injury, Thunderstrike, Dirt, Other Damage.

---

## Deployment Execution Manual

### Option A: Local Sandbox Environment Installation
To run the decoupled application layers natively on a local machine, execute the following steps via the terminal:

1. Navigate to the project root directory:
   cd final_project/

2. Initialize and activate the Conda environment:
   conda create -n uav_local python=3.10 -y && conda activate uav_local

3. Install the unified package dependencies:
   pip install -r requirements.txt

4. Boot Up Node 1 (FastAPI Backend Server):
   uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload

5. Boot Up Node 2 (Streamlit Frontend Dashboard):
   Open a second terminal window, activate the uav_local environment, and execute:
   streamlit run frontend/app.py

6. Access the Application: Open a web browser and navigate to http://localhost:8501/

### Option B: Isolated Containerized Deployment (Docker)
To compile the system into a standardized container vehicle:

1. Compile the Container Build Layout:
   docker build -t uav-drone-app .

2. Launch the Active Application Vehicle:
   docker run -d -p 8501:8501 --name live-uav-system uav-drone-app

3. Access the Container Portal: Open a web browser and navigate to http://localhost:8501/
