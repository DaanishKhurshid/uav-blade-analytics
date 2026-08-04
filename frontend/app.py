import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io
import os
import requests
from ultralytics import YOLO

st.set_page_config(
    page_title="UAV Drone Blade Analytics",
    page_icon="🛸",
    layout="wide"
)

st.title("🛸 Autonomous Wind Turbine Blade Inspection System")
st.write("Production-Grade Interface Running via Active Workspace Nodes.")

# 1. Configuration variables (WEB APP DEPLOYMENT CONFIGURATIONS SECURED)
FASTAPI_URL = "https://uav-backend-ffs9.onrender.com/predict"
MODEL_PATH = "frontend/final_production_model_50_epochs.pt"

CLASS_NAMES = {
    0: "corrosion", 1: "crack", 2: "craze", 3: "hide_craze",
    4: "surface_injure", 5: "thunderstrike", 6: "dirt", 7: "other_damage"
}

# 2. Deterministic SOP Knowledge Base (Derived from IEC 61400-23 & DNV-ST-0437 Standards)
SOP_REGISTRY = {
    "crack": {
        "standard_ref": "IEC 61400-23: Structural Testing of Rotor Blades",
        "severity": "CRITICAL RISK (LEVEL 5)",
        "protocol": "Immediate structural stabilization required. Initiate structural composite reinforcement injection.",
        "tools": "Ultrasonic non-destructive testing (NDT) array, vacuum-assisted resin transfer molding (VARTM) kit, structural epoxy resins.",
        "safety": "Lockout-Tagout (LOTO) engine rotation immediately. Clear 50-meter perimeter below nacelle for offshore support vessel drop zone."
    },
    "thunderstrike": {
        "standard_ref": "IEC 61400-24: Lightning Protection for Wind Turbines",
        "severity": "HIGH RISK (LEVEL 4)",
        "protocol": "Verify lightning protection system (LPS) continuity. Assess structural core de-lamination boundaries.",
        "tools": "Micro-ohmmeter conduction probe, thermal imaging UAV array, carbon-fiber patch matrix.",
        "safety": "Halt rotation within 12 hours. Ensure ground-fault monitoring arrays are active on the offshore substation deck."
    },
    "corrosion": {
        "standard_ref": "DNV-RP-0413: In-service Inspection of Wind Turbine Blades",
        "severity": "MEDIUM RISK (LEVEL 3)",
        "protocol": "Surface preparation via abrasive mechanical cleaning followed by localized anti-corrosive marine sealant re-coating.",
        "tools": "Low-pressure grit blaster, pneumatic composite sanders, ISO 12944 C5-M certified marine epoxy coatings.",
        "safety": "Standard offshore harness work coordinates. Ensure personal protective equipment (PPE) matches marine chemical hazards."
    },
    "surface_injure": {
        "standard_ref": "DNV-ST-0437: Structural Design of Wind Turbine Blades",
        "severity": "LOW RISK (LEVEL 2)",
        "protocol": "Localized leading-edge protection (LEP) tape application or micro-filler fairing compound surfacing.",
        "tools": "Polyurethane leading-edge protection tape, composite filler squeegees, UV curing lamps.",
        "safety": "Incorporate standard blade maintenance platform routing. Verify wind speeds are below 10 knots prior to crew deployment."
    }
}

# Default protocol for minor or cosmetic anomalies (craze, hide_craze, dirt, other_damage)
DEFAULT_SOP = {
    "standard_ref": "DNV-RP-0413: Routine Marine Asset Maintenance",
    "severity": "NOMINAL RISK (LEVEL 1)",
    "protocol": "Monitor anomaly progression during regular operational maintenance intervals.",
    "tools": "High-pressure clean water wash arrays, localized visual tracking camera frames.",
    "safety": "No emergency shutdown sequence required. Maintain standard automated grid synchronization."
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
        st.subheader("🔍 Automated AI Diagnostics & SOP Retrieval")
        
        success_processing = False
        
        # --- PATH A: TRY FASTAPI BACKEND STREAM FIRST ---
        try:
            files = {"file": (uploaded_file.name, raw_bytes, uploaded_file.type)}
            response = requests.post(FASTAPI_URL, files=files, timeout=5)
            
            if response.status_code == 200:
                st.info("⚡ Connection Secured: Processing via FastAPI Containerized Pipeline.")
                data = response.json()
                detections_count = data.get("defects_detected_count", 0)
                predictions = data.get("predictions", [])
                img_array = np.array(image)
                
                found_defect_names = []
                if detections_count == 0:
                    st.success("✅ Analysis Complete: No structural defects localized by FastAPI backend. Blade is flight-safe.")
                else:
                    st.warning(f"⚠️ Warning: FastAPI backend detected {detections_count} anomaly points.")
                    for pred in predictions:
                        name = pred["defect_name"]
                        found_defect_names.append(name)
                        conf = pred["confidence"]
                        xmin, ymin, xmax, ymax = pred["bounding_box"]
                        cv2.rectangle(img_array, (int(xmin), int(ymin)), (int(xmax), int(ymax)), (255, 0, 0), 4)
                        label = f"{name.upper()} ({conf*100:.1f}%)"
                        cv2.putText(img_array, label, (int(xmin), int(ymin) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
                
                st.image(img_array, use_container_width=True)
                
                # Match the highest-severity defect to our knowledge engine registry
                selected_sop = DEFAULT_SOP
                for core_defect in ["crack", "thunderstrike", "corrosion", "surface_injure"]:
                    if core_defect in found_defect_names:
                        selected_sop = SOP_REGISTRY[core_defect]
                        break
                
                st.write("---")
                st.subheader("🤖 Automated SOP Maintenance Agent Report")
                st.markdown(f"""
                ### 📂 Matched Engineering Standard: **{selected_sop['standard_ref']}**
                
                #### 🚨 Critical Level: `{selected_sop['severity']}`
                
                #### 🛠️ Actionable Field Maintenance Protocol
                {selected_sop['protocol']}
                
                #### 🔧 Required Tooling & Materials
                *{selected_sop['tools']}*
                
                #### 🦺 Mandatory Field Crew Safety Protocol
                **{selected_sop['safety']}**
                """)
                
                success_processing = True
                
        except Exception:
            pass # Move to fallback run smoothly

        # --- PATH B: FALLBACK NATIVE RUN ---
        if not success_processing:
            if os.path.exists(MODEL_PATH):
                st.success("💻 Standalone Mode Active: Running model parameters natively.")
                model_fallback = YOLO(MODEL_PATH)
                
                results = model_fallback.predict(source=image, imgsz=1024, conf=0.25, verbose=False)
                result = results[0]  
                detections_count = 0
                img_array = np.array(image)
                
                found_defect_names = []
                if result.boxes:
                    detections_count = len(result.boxes)
                    for i, box in enumerate(result.boxes):
                        xyxy = box.xyxy.tolist()[0]  
                        conf = float(box.conf[0])
                        cls_id = int(box.cls[0])
                        name = CLASS_NAMES.get(cls_id, "defect")
                        found_defect_names.append(name)
                        xmin, ymin, xmax, ymax = [int(coord) for coord in xyxy]
                        cv2.rectangle(img_array, (xmin, ymin), (xmax, ymax), (255, 0, 0), 4)
                        label = f"{name.upper()} ({conf*100:.1f}%)"
                        cv2.putText(img_array, label, (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
                
                if detections_count == 0:
                    st.success("✅ Analysis Complete: No structural defects localized. Blade is flight-safe.")
                else:
                    st.warning(f"⚠️ Warning: Detected {detections_count} anomaly points.")
                
                st.image(img_array, use_container_width=True)
                
                # Match the highest-severity defect to our knowledge engine registry for failover mode
                selected_sop = DEFAULT_SOP
                for core_defect in ["crack", "thunderstrike", "corrosion", "surface_injure"]:
                    if core_defect in found_defect_names:
                        selected_sop = SOP_REGISTRY[core_defect]
                        break
                
                st.write("---")
                st.subheader("🤖 Automated SOP Maintenance Agent Report")
                st.markdown(f"""
                ### 📂 Matched Engineering Standard: **{selected_sop['standard_ref']}**
                
                #### 🚨 Critical Level: `{selected_sop['severity']}`
                
                #### 🛠️ Actionable Field Maintenance Protocol
                {selected_sop['protocol']}
                
                #### 🔧 Required Tooling & Materials
                *{selected_sop['tools']}*
                
                #### 🦺 Mandatory Field Crew Safety Protocol
                **{selected_sop['safety']}**
                """)
            else:
                st.error("Critical Error: Unable to communicate with cloud or local fallback intelligence layers.")
