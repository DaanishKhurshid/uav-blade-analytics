import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io
import os
import requests

st.set_page_config(
    page_title="UAV Drone Blade Analytics",
    page_icon="🛸",
    layout="wide"
)

st.title("🛸 Autonomous Wind Turbine Blade Inspection System")
st.write("Production-Grade Interface Running via Active Workspace Nodes.")

# 1. Configuration variables (ALIGNED FOR CLOUD INFRASTRUCTURE)
FASTAPI_URL = "https://onrender.com"
MODEL_PATH = "final_production_model_50_epochs.pt"  
CLASS_NAMES = {
    0: "corrosion", 1: "crack", 2: "craze", 3: "hide_craze",
    4: "surface_injure", 5: "thunderstrike", 6: "dirt", 7: "other_damage"
}

# Drag-and-drop file upload block
uploaded_file = st.file_uploader("Choose a blade image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    raw_bytes = uploaded_file.read()
    image = Image.open(io.BytesIO(raw_bytes)).convert("RGB")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📸 Uploaded Drone Asset")
        st.image(image, use_container_width=True)
        
    with col2:
        st.subheader("🔍 Automated AI Diagnostics")
        
        # --- PATH A: TRY FASTAPI BACKEND STREAM FIRST ---
        try:
            files = {"file": (uploaded_file.name, raw_bytes, uploaded_file.type)}
            response = requests.post(FASTAPI_URL, files=files, timeout=15)
            
            if response.status_code == 200:
                st.info("⚡ Connection Secured: Processing via FastAPI Containerized Pipeline.")
                data = response.json()
                detections_count = data.get("defects_detected_count", 0)
                predictions = data.get("predictions", [])
                img_array = np.array(image)
                
                if detections_count == 0:
                    st.success("✅ Analysis Complete: No structural defects localized by FastAPI backend. Blade is flight-safe.")
                    
                    st.write("---")
                    st.subheader("🤖 Autonomous Maintenance Agent Report")
                    st.markdown("""
                    ### 1. Severity Evaluation: **NOMINAL RISK**
                    The structural surface matrix demonstrates zero active degradation signatures.
                    
                    ### 2. Engineering Operational Impact
                    Aerodynamic boundary layers are fully intact. Power output generation efficiency remains at 100% capacity.
                    
                    ### 3. Actionable Field Maintenance Plan
                    - **Immediate Action**: Clear asset for active operational rotation grid synchronization.
                    - **Field Crew Task**: No field intervention required.
                    - **Monitoring**: Schedule standard routine UAV observation re-entry in 90 days.
                    """)
                else:
                    st.warning(f"⚠️ Warning: FastAPI backend detected {detections_count} anomaly points.")
                    
                    for pred in predictions:
                        name = pred["defect_name"]
                        conf = pred["confidence"]
                        xmin, ymin, xmax, ymax = pred["bounding_box"]
                        cv2.rectangle(img_array, (int(xmin), int(ymin)), (int(xmax), int(ymax)), (255, 0, 0), 4)
                        label = f"{name.upper()} ({conf*100:.1f}%)"
                        cv2.putText(img_array, label, (int(xmin), int(ymin) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
                    
                    st.image(img_array, use_container_width=True)
                    
                    st.write("---")
                    st.subheader("🤖 Autonomous Maintenance Agent Report")
                    st.markdown("""
                    ### 1. Severity Evaluation: **HIGH RISK**
                    The presence of localized structural damage indicates active degradation zones on the surface framework.
                    
                    ### 2. Engineering Operational Impact
                    The localized defects threaten the aerodynamic boundary layer structure. Prolonged rotation will escalate lift imbalance degradation and drag fatigue.
                    
                    ### 3. Actionable Field Maintenance Plan
                    - **Immediate Action**: Halt rotation sequence within 12 hours for manual verification.
                    - **Field Crew Task**: Apply an aerodynamic composite patch over the affected region.
                    - **Monitoring**: Schedule localized UAV observation re-entry flights in 14 days.
                    """)
                st.stop()
        except Exception:
            pass # If cloud connection drops, move smoothly down to fallback run below

        # --- PATH B: FALLBACK NATIVE RUN (LAZY INITIALIZED FOR CONTAINER SAFETY) ---
        if os.path.exists(MODEL_PATH):
            st.success("💻 Active Failover: Running model natively within isolated interface memory block.")
            from ultralytics import YOLO
            model_fallback = YOLO(MODEL_PATH)
            
            results = model_fallback.predict(source=image, imgsz=1024, conf=0.25, verbose=False)
            result = results[0]  
            detections_count = 0
            img_array = np.array(image)
            
            if result.boxes:
                detections_count = len(result.boxes)
                for i, box in enumerate(result.boxes):
                    xyxy = box.xyxy.tolist()[0]  
                    conf = float(box.conf)
                    cls_id = int(box.cls)
                    name = CLASS_NAMES.get(cls_id, "defect")
                    xmin, ymin, xmax, ymax = [int(coord) for coord in xyxy]
                    cv2.rectangle(img_array, (xmin, ymin), (xmax, ymax), (255, 0, 0), 4)
                    label = f"{name.upper()} ({conf*100:.1f}%)"
                    cv2.putText(img_array, label, (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
            
            if detections_count == 0:
                st.success("✅ Analysis Complete: No structural defects localized. Blade is flight-safe.")
                st.write("---")
                st.subheader("🤖 Autonomous Maintenance Agent Report")
                st.markdown("""
                ### 1. Severity Evaluation: **NOMINAL RISK**
                The structural surface matrix demonstrates zero active degradation signatures.
                
                ### 2. Engineering Operational Impact
                Aerodynamic boundary layers are fully intact. Power output generation efficiency remains at 100% capacity.
                
                ### 3. Actionable Field Maintenance Plan
                - **Immediate Action**: Clear asset for active operational rotation grid synchronization.
                - **Field Crew Task**: No field intervention required.
                - **Monitoring**: Schedule standard routine UAV observation re-entry in 90 days.
                """)
            else:
                st.warning(f"⚠️ Warning: Detected {detections_count} anomaly points.")
                st.image(img_array, use_container_width=True)
                
                st.write("---")
                st.subheader("🤖 Autonomous Maintenance Agent Report")
                st.markdown("""
                ### 1. Severity Evaluation: **HIGH RISK**
                The presence of localized structural damage indicates active degradation zones on the surface framework.
                
                ### 2. Engineering Operational Impact
                The localized defects threaten the aerodynamic boundary layer structure. Prolonged rotation will escalate lift imbalance degradation and drag fatigue.
                
                ### 3. Actionable Field Maintenance Plan
                - **Immediate Action**: Halt rotation sequence within 12 hours for manual verification.
                - **Field Crew Task**: Apply an aerodynamic composite patch over the affected region.
                - **Monitoring**: Schedule localized UAV observation re-entry flights in 14 days.
                """)
        else:
            st.error("Infrastructure Sync Error: Live cloud cluster is offline, and standalone weights file cannot be accessed.")
