# 🐔 Chicken Disease Classification

## 🚀 Overview

This project leverages **deep learning** and **image processing** techniques to classify chicken diseases from images. It features a complete **end-to-end pipeline** including model training, Docker-based deployment, and a user-friendly React-based frontend for image uploads and disease predictions. A demo video is also included to showcase the development and deployment process.

---

## 🧠 Key Features

- Deep learning model to classify chicken diseases (e.g., **Salmonella**, **Coccidiosis**, **Newcastle Disease**)
- Dockerized backend with prediction pipeline
- React frontend for image upload and visualization
- Cross-platform and portable deployment
- Clean codebase with modular folder structure

---

## 📁 Project Structure

### 🧠 `Chicken-Disease-Classification/` (Backend)
```
├── data/                # Training dataset
│   ├── Train/
│   └── train_data.csv
├── logs/                # Training logs
├── models/              # Trained model files (.h5, .pkl)
├── src/
│   ├── components/      # Reusable backend components
│   ├── pipelines/       # Prediction pipeline
│   ├── utils/           # Helper scripts
│   └── temp/            # Temporary files
├── app.py               # Flask app entry point
├── Dockerfile           # Backend Docker config
├── requirements.txt     # Python dependencies
├── setup.py             # Python package configuration
├── .dockerignore
├── .python-version
└── chicken-disease-97-2.ipynb  # Jupyter notebook for model training
```

### 🌐 `chicken-disease-frontend/` (Frontend)
```
├── public/              # Static assets
├── src/
│   ├── components/      # React components (e.g., ImageUploader)
│   ├── App.js           # Main app
│   └── index.js         # Entry point
├── .env                 # Environment variables
├── Dockerfile           # Frontend Docker config
├── docker-compose.yml   # Orchestration file
├── package.json         # Project configuration
├── package-lock.json
├── README.md
└── demo_video.mp4       # Project walkthrough video
```

---

## 🛠️ Tech Stack

### 🔙 Backend
- **Python 3.10**
- **TensorFlow / Keras**
- **OpenCV** for image processing
- **Pandas**, **NumPy**, **Matplotlib**
- **Pickle** for model serialization
- **Flask** (if used in `app.py`)
- **Docker**

### 🔜 Frontend
- **React.js**
- **Node.js**
- **HTML/CSS**
- **Axios** (for API integration)

---

## 📊 Model Training

Training is performed using the `chicken-disease-97-2.ipynb` notebook:

- Loads and preprocesses data from `Train/` directory
- Visualizes image samples and label distribution
- Trains CNN models using TensorFlow/Keras
- Achieves high accuracy in classifying diseases
- Saves models in both `.h5` and `.pkl` formats for flexibility in deployment

---

## 🎥 Demo Video

📹 `[demo_video.mp4`  ](https://drive.google.com/file/d/1-gFX4ktcMwhKXjTf7IiejRiU4ob3thY9/view?usp=sharing)
Watch the included video for a full walkthrough of the training, development, and deployment process.

---

## ⚙️ Installation & Setup

### 🔧 Backend (Python)
```bash
git clone https://github.com/your-username/chicken-disease-classification.git
cd Chicken-Disease-Classification
pip install -r requirements.txt
cp .env.example .env  # Update as needed
docker-compose up --build
```

### 🌐 Frontend (React)
```bash
cd chicken-disease-frontend
npm install
npm start
```

> 💡 Access the app at `http://localhost:3000`

---

## 🧪 Usage

1. Open the frontend in your browser.
2. Upload a chicken image using the provided interface.
3. View predicted disease label and probability.
4. Use demo video for guidance if needed.

---

## 🤝 Contributing

Contributions are welcome!  
- Fork the repository  
- Create a feature branch  
- Submit a Pull Request  

Please follow standard commit and PR naming conventions.

---

## 👥 Made By

This project is developed by the following group members of IIIT Vadodara:

- 👩‍💻 **Smita Patel** – 202251129  
- 👩‍💻 **Niyati Pansuriya** – 202251080  
- 👨‍💻 **Sahil Sonker** – 202251115  
- 👩‍💻 **Shailly Yadav** – 202251123  

---

## 📄 License

_This project is currently unlicensed. Please add a license if open-sourcing._

---

## 📬 Contact

For issues, suggestions, or contributions, please [open an issue](https://github.com/your-repo/issues)
