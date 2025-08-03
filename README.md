# 🎥 Vision Forge 

**Vision Forge** is a real-time, OpenCV-powered web application built with Flask. It provides a suite of live webcam filters, face detection, augmented reality (AR) overlays (Currently just one).

## 🌐 Live Preview
[Click to Visit the Site](https://tasnim-ferdous.github.io/Websites/Pet%20Adoption%20Matching/index.html)

## 📷 Screenshot
![Vision Forge](https://hc-cdn.hel1.your-objectstorage.com/s/v3/1e522630da811ba2587e523f54c6a8b84cbc0eea_screenshot_3-8-2025_18415_127.0.0.1.jpeg)

## 🚀 Features

- 🔴 Live Webcam Preview
- 🎨 Real-Time Filters: Grayscale, Canny Edge, Invert, Blur, Thermal Cam Simulation
- 🧠 Face Detection with Bounding Boxes
- 🎭 Face Overlay Effects: Sunglasses
- 🎚️ Filter Intensity Control
- 🔳 Split View Mode (Original vs Filtered)
- 🖼️ Frame Capture & Download
- 🎛️ Interactive UI Controls
- 🧠 Modular Python Code for Extensibility

## 📁 Project Structure

```
visionforge/
├── Favicon/
│   └── tf.jpg
├── filters/
│   └── effects.py
├── haarcascades/
│   └── haarcascade_frontalface_default.xml
├── app.py
├── templates/
│   └── index.html
├── static/
│   ├── overlays/
|   |   └── sunglasses.png 
│   ├── scripts.js
│   └── styles.css
├── requirements.txt
├── Procfile
├── LICENSE
└── README.md
```

## ⚙️ Tech Stack

- **Frontend:** HTML, CSS, JavaScript (Vanilla)
- **Backend:** Flask (Python)
- **Computer Vision:** OpenCV
- **Deployment:** Render

## 🛠️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/visionforge.git
cd visionforge
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the app locally

```bash
python app.py
```

Then open [http://localhost:10000](http://localhost:10000) in your browser.

### 4. Deploy (Optional)

- **Recommended:** [Render.com](https://render.com)
- Add a `Procfile` with this content:

```
web: python app.py
```

- Set the port to `10000` in your Render service settings.

## 📜 License

[MIT License](LICENSE) © 2025 Md. Tasnim Ferdous

## ✨ Creator

Made with love by **Md. Tasnim Ferdous**  
💌 [tasnimferdous2007@gmail.com]  
🔗 [LinkedIn](https://www.linkedin.com/in/md-tasnimferdous/)

---

