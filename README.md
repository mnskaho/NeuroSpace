<div align="center">

# 🧠⚛️ NeuroSpace

### Classical AI vs Quantum Machine Learning Platform

**NeuroSpace** is an interactive web platform designed to compare classical machine learning models and quantum machine learning models for supervised classification tasks on numerical tabular datasets.

<br/>

![Next.js](https://img.shields.io/badge/Next.js-15-black?style=for-the-badge&logo=next.js)
![React](https://img.shields.io/badge/React-TypeScript-blue?style=for-the-badge&logo=react)
![FastAPI](https://img.shields.io/badge/FastAPI-Python-green?style=for-the-badge&logo=fastapi)
![Supabase](https://img.shields.io/badge/Supabase-PostgreSQL-3ECF8E?style=for-the-badge&logo=supabase)
![QML](https://img.shields.io/badge/Quantum-ML-purple?style=for-the-badge)
![License](https://img.shields.io/badge/License-CDDL%201.0-orange?style=for-the-badge)

</div>

---

## 📌 Overview

**NeuroSpace** is a web-based experimental platform that allows users to upload their own numerical datasets, train classical and quantum models, compare their performance, visualize the results, and generate downloadable reports.

The main objective of NeuroSpace is to make **Quantum Machine Learning (QML)** easier to test, understand, and evaluate, even for users who do not have advanced expertise in quantum computing.

---

## 🎯 Main Objective

NeuroSpace aims to answer the following question:

> **Can a quantum or hybrid quantum-classical model provide better results than a classical model on a given classification dataset?**

The platform does not assume that quantum models are always better.  
Instead, it provides a controlled experimental environment where classical and quantum models are trained and evaluated under the same conditions.

---

## 🧩 Project Description

NeuroSpace provides a complete environment for comparing:

- **Classical neural models**, such as Multilayer Perceptron (**MLP**)
- **Quantum or hybrid models**, such as Quantum Neural Networks (**QNN**)

The platform focuses on:

> **Numerical tabular datasets for supervised classification tasks**

This means that datasets can come from different domains such as:

- Healthcare
- Finance
- Banking
- Marketing
- Business
- Industry
- Education
- Scientific research

The only condition is that the dataset must be numerical, structured, and suitable for classification.

---

## 🚀 Main Features

- Upload numerical tabular datasets
- Validate dataset format and quality
- Detect missing values and incompatible data
- Preprocess data before training
- Train a classical MLP model
- Train a quantum or hybrid QNN model
- Compare models using classification metrics
- Display learning curves
- Generate confusion matrices
- Analyze model complexity
- Generate downloadable reports
- Support users from different domains

---

## 📊 Evaluation Metrics

NeuroSpace compares models using standard classification and complexity metrics:

| Category | Metrics |
|---|---|
| Classification | Accuracy, Precision, Recall, F1-score |
| Evaluation | Confusion Matrix, Classification Report |
| Complexity | Training Time, Inference Time |
| Quantum Model | Number of Qubits, Circuit Depth |
| Classical Model | Number of Parameters |

These metrics help users understand not only which model performs better, but also which model is more efficient and suitable for their dataset.

---

## 🏗️ Platform Architecture

NeuroSpace is based on a modular architecture.

```text
User Interface
     |
     v
Dataset Upload & Validation
     |
     v
Preprocessing Pipeline
     |
     v
Classical ML Model  <---->  Quantum ML Model
     |
     v
Evaluation & Comparison
     |
     v
Visualizations + Reports

The frontend allows users to interact with the platform through a simple web interface.
The backend manages dataset processing, training jobs, model execution, and result storage.
The machine learning and quantum learning modules are executed through Python-based workflows.

🔁 Workflow

The general workflow of NeuroSpace is:

User creates an account or logs in.
User uploads a numerical dataset.
The platform validates the dataset.
The dataset is preprocessed.
A classical MLP model is trained.
A QNN model is trained.
The models are evaluated.
The results are compared.
The user views metrics, graphs, and reports.
The final report can be downloaded.
📂 Dataset Requirements

The uploaded dataset must respect the following conditions:

CSV format
Numerical values only
No missing values
Structured tabular format
Suitable for supervised classification
Contains input features and a target class

Examples of compatible datasets:

Breast Cancer classification dataset
Heart Disease classification dataset
Dermatology classification dataset
Credit risk classification dataset
Customer profile classification dataset
Medical diagnosis classification dataset
🧪 Example Use Cases
🏦 Banking

A bank can upload a numerical tabular dataset containing customer information.
NeuroSpace can compare a classical MLP model and a quantum QNN model to classify customer risk categories.

🏥 Healthcare

A researcher can upload a medical dataset and compare classical and quantum models for disease classification.

📈 Marketing

A marketing team can upload customer data to classify users into different groups based on behavior or profile.

🛠️ Technologies Used
Frontend
Next.js
React
TypeScript
Tailwind CSS
Recharts
Backend
FastAPI
Python
REST API
Database and Authentication
Supabase
PostgreSQL
Supabase Auth
Supabase Storage
Machine Learning
Python
Scikit-learn
PyTorch
NumPy
Pandas
Quantum Machine Learning
PennyLane
Qiskit
Parameterized Quantum Circuits
Quantum Neural Networks
Angle Encoding
Deployment and Tools
GitHub
Vercel
Google Colab
ngrok
PayPal
Email notification system
📈 Results and Reports

After training and evaluation, NeuroSpace displays:

Classification metrics
Confusion matrix
Accuracy and loss curves
Model comparison table
Complexity analysis
Downloadable report

The generated report helps users understand the strengths and limitations of each model.

⚙️ Installation
Prerequisites

Before running the project locally, make sure you have:

Node.js installed
Python installed
Git installed
A Supabase account
A Python virtual environment
Required environment variables
💻 Frontend Installation
git clone https://github.com/mnskaho/NeuroSpace.git
cd NeuroSpace
npm install
npm run dev

The frontend will usually run on:

http://localhost:3000
🐍 Backend Installation

Go to the backend folder:

cd backend

Create a virtual environment:

python -m venv venv

Activate the environment:

venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Run the backend:

uvicorn main:app --reload

The backend will usually run on:

http://localhost:8000
🔐 Environment Variables

Create a .env file and add the required keys:

NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
SUPABASE_SERVICE_ROLE_KEY=
BACKEND_URL=
PAYPAL_CLIENT_ID=
EMAIL_SERVICE_KEY=

Do not upload your .env file to GitHub.

🚫 Files to Ignore

Before pushing the project to GitHub, make sure these files and folders are ignored:

node_modules/
.next/
.env
.env.local
__pycache__/
venv/

Add them to .gitignore.

🔮 Future Work

Future improvements of NeuroSpace include:

Adding more classical machine learning models
Adding more quantum model architectures
Improving the dashboard and visualizations
Supporting image classification using CNN models
Adding advanced model recommendation features
Integrating real quantum machines through IBM Quantum if financial and technical resources become available
Extending the platform for wider national and international use
👥 Authors

This project was developed by:

Horchi Abir Selma
Kadri Manel
Kadri Nourhene

Supervised by:

Dr. Khadir Mohamed Tarek

Academic affiliation:

University Badji Mokhtar – Annaba
Faculty of Technology
Department of Computer Science
Master 2 SID
