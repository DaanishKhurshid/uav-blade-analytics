import io
import os
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from PIL import Image
from ultralytics import YOLO

app = FastAPI(
    title="UAV Wind Turbine Blade Inspection API",
    description="Production-grade FastAPI backend for localized object detection.",
    version="1.0.0"
)

# Direct path to your weights inside your clean local folder layout
MODEL_PATH = "final_production_model_50_epochs.pt"



# Load the model directly into local system runtime memory
if os.path.exists(MODEL_PATH):
    model = YOLO(MODEL_PATH)
else:
    raise FileNotFoundError(f"Critical Error: Cannot locate model weights at {MODEL_PATH}")

# Human-readable dictionary mapping numbers back to names
CLASS_NAMES = {
    0: "corrosion", 1: "crack", 2: "craze", 3: "hide_craze",
    4: "surface_injure", 5: "thunderstrike", 6: "dirt", 7: "other_damage"
}

@app.get("/")
def root():
    return {"status": "online", "model_loaded": True, "resolution": "1024x1024"}

@app.post("/predict")
async def predict_blade_defect(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        raise HTTPException(status_code=400, detail="Invalid image format. Please upload a JPG or PNG.")
        
    try:
        # Read incoming raw image file bytes safely in memory
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        
        # Run 1024x1024 high-resolution prediction
        results = model.predict(source=image, imgsz=1024, conf=0.25, verbose=False)
        result = results[0]  # Extract the first element array
        
        detections = []
        
        if result.boxes:
            for box in result.boxes:
                xyxy = box.xyxy.tolist()[0]  # [xmin, ymin, xmax, ymax]
                conf = float(box.conf[0])
                cls_id = int(box.cls[0])
                
                detections.append({
                    "class_id": cls_id,
                    "defect_name": CLASS_NAMES.get(cls_id, "unknown"),
                    "confidence": round(conf, 4),
                    "bounding_box": [round(coord, 2) for coord in xyxy]
                })
                
        return JSONResponse(content={
            "filename": file.filename,
            "defects_detected_count": len(detections),
            "predictions": detections
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal API processing error: {str(e)}")
