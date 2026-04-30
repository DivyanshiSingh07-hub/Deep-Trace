# DeepTrace — Complete Project

## Folder structure
```
Deep-Trace/
├── backend/
│   ├── app.py                         ← FastAPI backend
│   ├── requirements.txt
│   ├── deepfake_pytorch_gpu_e2e.ipynb ← Fixed training notebook
│   └── deepfake_detector_v1.pth       ← Your trained weights (place here)
└── frontend/
    └── index.html                     ← Complete frontend (no build step)
```

---

## Step 1 — Retrain (recommended)

Open `deepfake_pytorch_gpu_e2e.ipynb` and update **CELL 3 CONFIG only**:

```python
CELEB_REAL_DIR  = r'D:\...\CelebDF\Celeb-real'
CELEB_FAKE_DIR  = r'D:\...\CelebDF\Celeb-synthesis'
DATA_DIR        = r'D:\...\backend\deepfake_dataset'
MODEL_OUT       = r'D:\...\backend\deepfake_detector_v1.pth'
VIDEOS_PER_CLASS = 300   # use as many as you have
```

Run all cells top to bottom. The notebook will:
- Split videos into train/val **by video** (no leakage)
- Extract 10 frames per video
- Train EfficientNet-B0 with normalization
- Save the best model automatically
- Show confusion matrix and training curves

**Do NOT mix in CIFAKE** — it confuses the model.

---

## Step 2 — Configure backend

Open `backend/app.py` and check the CONFIG section at the top:

```python
MODEL_TYPE    = 'efficientnet'   # matches the new notebook
WEIGHT_FILE   = 'deepfake_detector_v1.pth'
USE_NORMALIZE = True             # must match training
THRESHOLD     = 0.5
```

If you ever switch back to the old custom CNN:
```python
MODEL_TYPE    = 'deepfakecnn'
USE_NORMALIZE = False   # old model had no normalize
```
**That's the only change needed — frontend adapts automatically.**

---

## Step 3 — Run backend

```bash
cd backend
pip install -r requirements.txt
python app.py
# → http://localhost:8000
```

Verify:
```
GET http://localhost:8000/health
→ { "status": "ok", "model_type": "efficientnet", "weights_loaded": true, ... }
```

---

## Step 4 — Run frontend

```bash
cd frontend
python -m http.server 5500
# → Open http://localhost:5500
```

Or open `index.html` directly in Firefox (Chrome blocks fetch from file://).

---

## Changing your model in future

The frontend and backend are decoupled. When you retrain:

1. Save new weights as `deepfake_detector_v1.pth` in `backend/`
2. Update `MODEL_TYPE` and `USE_NORMALIZE` in `app.py` CONFIG
3. Restart backend: `python app.py`
4. **No frontend changes needed** — it reads model info from `/health`

---

## API reference

| Method | Route | Description |
|--------|-------|-------------|
| GET | /health | Status, GPU, model type, weights loaded |
| POST | /predict | Upload file → prediction JSON |

### /predict response
```json
{
  "prediction":     "FAKE",
  "confidence":     91.23,
  "frames_analyzed": 9,
  "raw_probability": 0.0877,
  "model_type":     "efficientnet"
}
```
`raw_probability > 0.5 → REAL` (fake=0, real=1 from ImageFolder alphabetical order)

---

## Why predictions were wrong before

| Issue | Fix applied |
|-------|-------------|
| Model trained without Normalize, backend added it | Normalize removed from old path; new training adds it consistently |
| Labels flipped (fake=0, real=1 but code said >0.5=FAKE) | Fixed: `>0.5 → REAL` |
| CIFAKE (32px animals) mixed with CelebDF (face videos) | CIFAKE removed entirely |
| Only 100 videos per class → memorized, not learned | New notebook uses 300+ with proper video-level split |
| Custom CNN too small to generalize | Replaced with EfficientNet-B0 (pretrained ImageNet) |
