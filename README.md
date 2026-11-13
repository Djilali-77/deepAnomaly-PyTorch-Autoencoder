# 🛡️ DeepAnomaly: AI-Powered Network Security Dashboard

![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker&logoColor=white)
![React](https://img.shields.io/badge/React-Frontend-61DAFB?logo=react&logoColor=black)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-Deep%20Learning-EE4C2C?style=flat&logo=pytorch&logoColor=white)

An End-to-End, Full-Stack MLOps project that leverages Unsupervised Machine Learning (**Deep Autoencoders in PyTorch**) to detect zero-day network anomalies and malicious intrusions. Trained on the **UNSW-NB15** dataset, this system features a decoupled FastAPI backend, a modern React (Vite) Security Operations Center (SOC) dashboard, and is fully containerized using **Docker** for seamless production deployment.

## 🌟 Key Features
- **Real-Time Anomaly Detection:** Utilizes Mean Squared Error (MSE) reconstruction loss to identify abnormal network packets. Traffic that exceeds a dynamically tuned threshold is instantly flagged.
- **Interactive Packet Simulator:** Users can manually inject the 5 most critical network flow parameters (`sttl`, `ct_state_ttl`, `sbytes`, `dbytes`, `smean`) via an interactive cyber-themed React dashboard.
- **Smart Feature Filling:** The autoencoder expects 65 features. The dashboard asks for 5 of them (`sttl`, `ct_state_ttl`, `sbytes`, `dbytes`, `smean`) and the API fills the rest with the median of normal training traffic, then applies the same log transform and scaling used in training.
- **Dockerized Architecture:** The entire stack (React frontend and PyTorch/FastAPI backend) is containerized, eliminating environment conflicts and ensuring a smooth "plug-and-play" experience across all operating systems.

## 🏗️ System Architecture
The machine learning pipeline is built with a modular, production-ready Object-Oriented design:
1. **Data Pipeline:** Ingests the raw UNSW-NB15 CSV files, cleans NaN values, and applies `MinMaxScaler` and One-Hot Encoding.
2. **PyTorch Autoencoder:** A deep neural network trained exclusively on benign traffic to learn the blueprint of normal network behavior.
3. **Threshold Selection:** 10% of the normal training traffic is kept aside as a validation set. The anomaly threshold is the 95th percentile of the reconstruction errors on that set (`0.001417`), saved at training time and loaded by the API.
4. **API Backend:** A multi-file FastAPI architecture (`main.py`, `routes.py`, `services.py`, `schemas.py`) utilizing Pydantic for strict payload validation.
5. **Frontend SOC Dashboard:** A Framer Motion-animated React dashboard powered by TailwindCSS to visualize system states (Secure vs. Critical Attack).

## 🧠 Engineering Challenges Solved
- **Metrics that looked like random guessing:** The first version scored about 49% accuracy. The cause was a bug, not the model: the test DataLoader shuffled the rows, but the labels stayed in file order, so every error was compared to the wrong label. The first sign was precision of 0.55, equal to the share of attacks in the test set. After turning shuffling off, accuracy went from 49% to 82%.
- **Heavy-tailed features:** Columns like `sbytes` reach millions, so `MinMaxScaler` squeezed almost every flow near zero. A `log1p` transform on those columns made the scaled features much more useful for the autoencoder.
- **Threshold chosen without peeking at the test set:** The old threshold was set by hand. It is now the 95th percentile of the errors on held-out normal traffic, and the training script saves it so the API and the training always use the same value.
- **Training-serving consistency:** The API now uses the same column order, log transform and scaler as training, and fills missing features with the median of normal traffic instead of zeros.

## 🛠️ Tech Stack

| Domain | Technologies Used |
| :--- | :--- |
| **Machine Learning** | Python, **PyTorch**, Scikit-Learn (MinMaxScaler), Pandas, Numpy, Joblib |
| **Backend API** | FastAPI, Uvicorn, Pydantic |
| **Frontend Dashboard**| React.js (Vite), TailwindCSS, Framer Motion |
| **DevOps / Deployment** | Docker, Docker-Compose |

## 📊 Results (UNSW-NB15 test set)

| Metric | Value |
| :--- | :--- |
| Accuracy | 81.72% |
| Precision | 91.42% |
| Recall | 73.72% |
| F1-Score | 81.62% |
| False Positive Rate | 8.48% |
| ROC-AUC | 0.8888 |
| PR-AUC | 0.9185 |

The model is trained only on normal traffic, so it needs no attack labels. Attacks are found only because their reconstruction error is higher than normal.

## ⚠️ Limitations
- Recall is 73.7%, so about 1 attack in 4 is missed.
- The false positive rate is 8.5%, higher than the 5% expected from the threshold, because test traffic differs a little from training traffic.
- The dashboard sends only 5 features, so the other 60 are filled with typical normal values. It is a demo, not full flow analysis.
- Not yet measured: which attack categories are missed the most.

### Retrain the model
Download UNSW-NB15 and put the CSV files in `backend/data/`, then run:
​```bash
cd backend/src
python train_pipeline.py
​```

### Prerequisites
- [Docker](https://www.docker.com/products/docker-desktop/) installed and running on your machine.

### Installation & Execution
1. **Clone the repository:**
   ```bash
   git clone https://github.com/Djilali-77/l2-DeepAnomaly-PyTorch-Autoencoder.git
   cd l2-DeepAnomaly-PyTorch-Autoencoder
   ```

2. **Build and start the application:**
   *(Note: The initial build downloads the PyTorch CPU wheels and may take a few minutes depending on your internet connection. Subsequent builds are instant).*
   ```bash
   docker-compose up --build
   ```

3. **Access the application:**
- **Frontend SOC Dashboard:** Open your browser and navigate to 👉 `http://localhost:5173`
- **Backend API (Swagger UI):** Open your browser and navigate to 👉 `http://localhost:8000/docs`

> **Note for Mac users:** If Safari fails to connect to `localhost:5173`, simply use `http://127.0.0.1:5173` instead.

### 🛑 How to Stop the Application
To safely shut down the containers and free up the ports, press `Ctrl+C` in the terminal, then run:
```bash
docker-compose down
```
