# 🌱 EcoScan AI — Land & Soil Analysis

> **AI-powered environmental intelligence for vegetation analysis and soil-type detection.**

EcoScan AI is a web-based application that uses **Deep Learning and Computer Vision** to analyze environmental images. The application provides two core AI capabilities:

* 🌿 **Vegetation Segmentation** — estimates the percentage of green/vegetated area in an uploaded image.
* 🪨 **Soil Type Detection** — identifies the soil type from an uploaded soil image and provides the model confidence.

The application combines a lightweight web interface with a **Flask REST API** and pre-trained deep learning models.

---

## 🚀 Live Demo

### 🌐 EcoScan AI — Land & Soil Analysis

**Live Application:**
[https://eco-scan-friendly-kpkuv592r-hemalatha0303s-projects.vercel.app/](https://eco-scan-friendly-kpkuv592r-hemalatha0303s-projects.vercel.app/)

The frontend is deployed on **Vercel**, while the AI backend is deployed on **Render**.

---

## ✨ Features

### 🌿 Vegetation Analysis

Upload an environmental or land image to estimate green/vegetated coverage.

The application:

1. Accepts an image from the user.
2. Converts the image to RGB.
3. Resizes it to `256 × 256`.
4. Normalizes pixel values.
5. Passes the image through the vegetation segmentation model.
6. Applies a `0.5` threshold to the predicted mask.
7. Calculates the percentage of pixels classified as vegetation.

### 🪨 Soil Type Detection

Upload a soil image to identify its soil type.

The application:

1. Accepts the uploaded image.
2. Sends it to the Flask backend.
3. Runs the YOLO model.
4. Extracts the detected class.
5. Extracts the prediction confidence.
6. Returns the predicted soil type and confidence percentage.

### 🖼️ Image Preview

Uploaded images are displayed in the browser before running the AI analysis.

### 🔌 REST API

The backend exposes separate API endpoints for vegetation and soil analysis.

### ⚡ Lazy Model Loading

The AI models are loaded only when they are required instead of loading everything immediately when the Flask application starts.

This reduces unnecessary startup work and makes the application more suitable for cloud deployment.

### 🌐 Cloud Deployment

The architecture separates the frontend and backend:

```text
User
 │
 ▼
Vercel
Frontend
 │
 │ HTTPS API Request
 ▼
Render
Flask Backend
 │
 ├── U-Net / Keras Model
 │
 └── YOLOv8 Model
```

---

# 🧠 AI Models

## 1. Vegetation Segmentation

EcoScan AI uses a pre-trained **TensorFlow/Keras segmentation model** for vegetation analysis.

The model is loaded from:

```text
backend/models/vegetation_model.h5
```

### Image preprocessing

Input images are:

* Converted to RGB
* Resized to `256 × 256`
* Converted to `float32`
* Normalized to the `[0, 1]` range
* Expanded with a batch dimension

The preprocessing pipeline is implemented in:

```text
backend/app.py
```

### Green Coverage Calculation

After prediction, the output is clipped to the range:

```text
0 → 1
```

A threshold of:

```text
0.5
```

is applied to generate the binary vegetation mask.

The coverage is calculated as:

```text
Vegetation Coverage =
(Number of vegetation pixels / Total pixels) × 100
```

The API returns the result rounded to two decimal places.

Example:

```json
{
  "status": "success",
  "coverage": 64.27
}
```

---

## 2. Soil Type Detection

EcoScan AI uses a **YOLO-based object detection model** for soil classification.

The model is stored at:

```text
backend/models/best.pt
```

The model is loaded using:

```python
from ultralytics import YOLO
```

The first detected bounding box is used to obtain:

* Class ID
* Soil label
* Confidence score

Example API response:

```json
{
  "status": "success",
  "label": "Black Soil",
  "confidence": 0.9234
}
```

The frontend converts the confidence into a percentage:

```text
92.34%
```

If no detection is found, the backend returns:

```json
{
  "status": "not_detected",
  "label": "Unknown",
  "confidence": 0
}
```

---

# 🏗️ Project Architecture

```text
EcoScan AI
│
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── style.css
│
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   └── models/
│       ├── best.pt
│       └── vegetation_model.h5
│
├── .gitignore
└── .gitattributes
```

---

# 📁 Directory Structure

```text
eco_scan_friendly_app/
│
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   │
│   └── models/
│       ├── best.pt
│       └── vegetation_model.h5
│
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── style.css
│
├── .gitignore
└── .gitattributes
```

---

# 🔧 Technology Stack

## Frontend

* HTML5
* CSS3
* JavaScript
* Fetch API
* FileReader API
* Google Fonts — Inter

## Backend

* Python
* Flask
* Flask-CORS
* Gunicorn

## Artificial Intelligence

* TensorFlow
* Keras
* YOLO
* Ultralytics
* OpenCV
* NumPy
* Pillow

## Deployment

* Vercel — Frontend
* Render — Backend

---

# 🔄 Application Workflow

## Vegetation Analysis

```text
Upload Image
     │
     ▼
Browser Image Preview
     │
     ▼
JavaScript FormData
     │
     ▼
POST /predict/vegetation
     │
     ▼
Flask Backend
     │
     ▼
Image Preprocessing
     │
     ▼
Keras Segmentation Model
     │
     ▼
Binary Vegetation Mask
     │
     ▼
Coverage Calculation
     │
     ▼
Green Coverage %
     │
     ▼
Frontend Result
```

---

## Soil Analysis

```text
Upload Soil Image
       │
       ▼
Browser Image Preview
       │
       ▼
JavaScript FormData
       │
       ▼
POST /predict/soil
       │
       ▼
Flask Backend
       │
       ▼
YOLO Model
       │
       ▼
Detection
       │
       ├── No Detection
       │       │
       │       ▼
       │    Unknown
       │
       └── Detection
               │
               ▼
        Soil Type + Confidence
               │
               ▼
          Frontend Result
```

---

# 🔌 API Documentation

## Base URL

The frontend is configured to communicate with the deployed Render backend.

```text
https://eco-scan-friendly-app.onrender.com
```

---

## Health Check

### `GET /`

Checks whether the Flask backend is running.

### Response

```text
EcoScan AI Backend Running
```

---

## Model Warmup

### `GET /warmup`

Loads both AI models into memory.

### Response

```text
Models loaded
```

This endpoint can be useful after deployment to initialize the models before sending prediction requests.

---

## Vegetation Prediction

### `POST /predict/vegetation`

Accepts an image and calculates estimated green coverage.

### Request

```text
Content-Type: multipart/form-data
```

Parameter:

```text
file
```

### Example Response

```json
{
  "status": "success",
  "coverage": 72.45
}
```

### Possible Error

```json
{
  "error": "No file uploaded"
}
```

---

## Soil Prediction

### `POST /predict/soil`

Accepts a soil image and predicts its class.

### Request

```text
Content-Type: multipart/form-data
```

Parameter:

```text
file
```

### Example Response

```json
{
  "status": "success",
  "label": "Red Soil",
  "confidence": 0.9142
}
```

### No Detection

```json
{
  "status": "not_detected",
  "label": "Unknown",
  "confidence": 0
}
```

---

# 💻 Running Locally

## 1. Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd eco_scan_friendly_app
```

---

## 2. Create a Virtual Environment

Navigate to the backend:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Linux/macOS

```bash
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

The backend dependencies include:

```text
Flask
Flask-CORS
Gunicorn
NumPy
OpenCV
Pillow
TensorFlow
Ultralytics
```

---

## 4. Start the Backend

From the `backend` directory:

```bash
python app.py
```

The application uses port `10000` by default.

Backend:

```text
http://127.0.0.1:10000
```

---

## 5. Configure the Frontend

Open:

```text
frontend/script.js
```

For local development, change:

```javascript
const API_BASE = "https://eco-scan-friendly-app.onrender.com";
```

to:

```javascript
const API_BASE = "http://127.0.0.1:10000";
```

---

## 6. Run the Frontend

Open:

```text
frontend/index.html
```

in a browser, or serve the frontend using a local HTTP server.

For example:

```bash
cd frontend
python -m http.server 5500
```

Then open:

```text
http://127.0.0.1:5500
```

---

# ☁️ Deployment

## Frontend — Vercel

The frontend consists of static:

```text
HTML
CSS
JavaScript
```

and can therefore be deployed as a static frontend.

Live deployment:

```text
https://eco-scan-friendly-kpkuv592r-hemalatha0303s-projects.vercel.app/
```

---

## Backend — Render

The Flask API is deployed separately.

Backend URL configured in the frontend:

```text
https://eco-scan-friendly-app.onrender.com
```

The Flask application reads the deployment port from the environment:

```python
port = int(os.environ.get("PORT", 10000))
```

and runs on:

```python
app.run(host="0.0.0.0", port=port)
```

For a production deployment, Gunicorn can be used to serve the Flask application.

---

# 🔐 CORS

The Flask backend uses Flask-CORS:

```python
CORS(app)
```

This allows the separately deployed Vercel frontend to communicate with the Render backend.

---

# 🎨 User Interface

The application contains three main sections:

### 🏠 Home

Introduces EcoScan AI and provides navigation to the two analysis modules.

### 🌿 Vegetation

Allows users to upload an environmental image and estimate green coverage.

### 🪨 Soil Type

Allows users to upload a soil image and identify the predicted soil type.

The interface uses a clean environmental theme with green, black, and white colors.

---

# 📊 Example Use Cases

EcoScan AI can serve as a prototype for:

* 🌱 Vegetation monitoring
* 🌳 Green-cover estimation
* 🏞️ Land analysis
* 🌾 Agricultural image analysis
* 🪨 Soil classification
* 🌍 Environmental monitoring
* 🔬 Computer Vision demonstrations
* 🎓 AI/ML academic projects
* 🚀 AI-powered sustainability applications

---

# ⚠️ Limitations

EcoScan AI is an AI-based prototype and its predictions depend heavily on the quality and distribution of the data used to train the underlying models.

### Vegetation Analysis

The reported green coverage is an **estimated segmentation-based measurement**, not a certified environmental measurement.

Different lighting conditions, image angles, shadows, vegetation types, and image quality can affect the result.

### Soil Detection

The soil classification model can only reliably identify classes represented in its training data.

Images that are significantly different from the training distribution may produce incorrect or low-confidence predictions.

### No Detection

If the YOLO model does not detect an object, the application returns:

```text
Unknown
```

rather than forcing a classification.

---

# 🔒 Privacy

Images uploaded to the application are sent to the deployed backend for AI inference.

The application does not implement permanent image storage in the provided backend code.

However, users should avoid uploading sensitive or private images because deployment infrastructure and server logs may have their own retention policies.

---

# 🧪 Error Handling

The backend checks whether an image has been uploaded before processing.

If no file is supplied:

```json
{
  "error": "No file uploaded"
}
```

Unexpected backend or model errors return an HTTP `500` response.

The frontend catches API failures and displays:

```text
Backend not reachable or model error.
Check Render logs.
```

---

# 📌 Important Project Files

| File                                 | Purpose                              |
| ------------------------------------ | ------------------------------------ |
| `backend/app.py`                     | Flask API and AI inference logic     |
| `backend/requirements.txt`           | Python dependencies                  |
| `backend/models/best.pt`             | YOLO soil detection model            |
| `backend/models/vegetation_model.h5` | Keras vegetation segmentation model  |
| `frontend/index.html`                | Application structure                |
| `frontend/script.js`                 | Frontend logic and API communication |
| `frontend/style.css`                 | UI styling                           |
| `.gitignore`                         | Files excluded from Git              |

---

# 🎯 Project Highlights

### Artificial Intelligence

* TensorFlow/Keras
* Image segmentation
* YOLO-based computer vision
* Confidence-based prediction

### Backend Development

* Flask REST API
* Multipart image upload
* Model inference APIs
* Lazy model loading
* CORS configuration

### Frontend Development

* Responsive HTML/CSS interface
* Vanilla JavaScript
* File upload
* Image preview
* Asynchronous API requests

### Cloud Deployment

* Vercel frontend deployment
* Render backend deployment
* Frontend-backend separation
* Cloud-hosted AI inference

---

# 👩‍💻 Author

**Hemalatha Donapati**

B.Tech — Artificial Intelligence & Machine Learning

### Project

**EcoScan AI — Land & Soil Analysis**

---

# ⭐ Acknowledgment

This project demonstrates the integration of **Artificial Intelligence, Computer Vision, REST APIs, and Cloud Deployment** into an environmental analysis application.

If you find the project useful, consider giving the repository a ⭐ on GitHub.
