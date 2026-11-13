# 🛡️ DeepAnomaly: AI-Powered Network Security Dashboard

![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker&logoColor=white)
![React](https://img.shields.io/badge/React-Frontend-61DAFB?logo=react&logoColor=black)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-Deep%20Learning-EE4C2C?style=flat&logo=pytorch&logoColor=white)

An End-to-End, Full-Stack MLOps project that leverages Unsupervised Machine Learning (**Deep Autoencoders in PyTorch**) to detect zero-day network anomalies and malicious intrusions. Trained on the **UNSW-NB15** dataset, this system features a decoupled FastAPI backend, a modern React (Vite) Security Operations Center (SOC) dashboard, and is fully containerized using **Docker** for seamless production deployment.

## 🌟 Key Features
- **Real-Time Anomaly Detection:** Utilizes Mean Squared Error (MSE) reconstruction loss to identify abnormal network packets. Traffic that exceeds a dynamically tuned threshold is instantly flagged.
- **Interactive Packet Simulator:** Users can manually inject the 5 most critical network flow parameters (`sttl`, `ct_state_ttl`, `sbytes`, `dbytes`, `smean`) via an interactive cyber-themed React dashboard.
- **Smart Feature Padding:** The trained autoencoder expects exactly 65 features (due to one-hot encoding). To drastically improve User Experience (UX), the API dynamically injects a zero-padded baseline for the missing 60 features in the background, allowing inference on partial data without breaking the strict scaler.
- **Dockerized Architecture:** The entire stack (React frontend and PyTorch/FastAPI backend) is containerized, eliminating environment conflicts and ensuring a smooth "plug-and-play" experience across all operating systems.

## 🏗️ System Architecture
The machine learning pipeline is built with a modular, production-ready Object-Oriented design:
1. **Data Pipeline:** Ingests the raw UNSW-NB15 CSV files, cleans NaN values, and applies `MinMaxScaler` and One-Hot Encoding.
2. **PyTorch Autoencoder:** A deep neural network trained exclusively on benign traffic to learn the blueprint of normal network behavior.
3. **Threshold Tuning Engine:** Establishes a baseline reconstruction loss (`0.0709`) and dynamically sets a rigid boundary (`0.073`) to catch simulated attacker footprints (e.g., unusual `sttl` values).
4. **API Backend:** A multi-file FastAPI architecture (`main.py`, `routes.py`, `services.py`, `schemas.py`) utilizing Pydantic for strict payload validation.
5. **Frontend SOC Dashboard:** A Framer Motion-animated React dashboard powered by TailwindCSS to visualize system states (Secure vs. Critical Attack).

## 🧠 MLOps & Engineering Challenges Solved
- **Dynamic Dimension Matching (The 65 vs 45 Feature Problem):** During production deployment, a dimension mismatch occurred because preprocessing (One-Hot Encoding) expanded the feature space from 45 to 65 columns. I refactored the API inference logic to map the user's 5 inputs to the correct tensor indices while zero-padding the rest, effectively tricking the strict PyTorch model into accepting live user inputs.
- **Precision Thresholding for Edge Cases:** Setting the MSE anomaly threshold too high caused false negatives, while setting it too low triggered alerts on missing data. By isolating normal behavior (loss `0.0709`) and simulating an Nmap footprint (`sttl=252`), I calibrated the threshold to exactly `0.08`, achieving a perfect balance between sensitivity and stability.
- **Optimized PyTorch Containerization:** Standard PyTorch Docker images are notoriously heavy (>3GB). To optimize CI/CD and local builds, I configured the `Dockerfile` to strictly pull the CPU-only wheels on top of a `python:3.10-slim` base image, slashing the backend container size and build time while maintaining lightning-fast inference speeds. Resolving `Node 22` engine constraints further future-proofed the modern Vite frontend.

## 🛠️ Tech Stack

| Domain | Technologies Used |
| :--- | :--- |
| **Machine Learning** | Python, **PyTorch**, Scikit-Learn (MinMaxScaler), Pandas, Numpy, Joblib |
| **Backend API** | FastAPI, Uvicorn, Pydantic |
| **Frontend Dashboard**| React.js (Vite), TailwindCSS, Framer Motion |
| **DevOps / Deployment** | Docker, Docker-Compose |

## 🚀 How to Run the Project

Because the entire application is containerized, you don't need to install Python, Node.js, or heavy ML libraries like PyTorch on your local machine.

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
