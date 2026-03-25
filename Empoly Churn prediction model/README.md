# 🚀 Customer Churn Prediction System (Real-Time ML Analytics Dashboard)

## 📌 Overview

This project is a **complete end-to-end Machine Learning system** that predicts customer churn and visualizes insights in real time. It simulates a real-world business application where companies monitor customer behavior, generate predictions, and make data-driven decisions.

The system integrates:

* 🤖 Machine Learning (Prediction)
* ⚙️ FastAPI (Backend APIs)
* 🗄 PostgreSQL (Database)
* 📊 Streamlit (Dashboard)

---

## 🎯 Objectives

* Accept and store customer data
* Process and transform data for ML usage
* Generate churn predictions using a trained model
* Store predictions in a database
* Display insights dynamically on a dashboard

---

## 🧠 Problem Statement

Customer churn is a critical problem in industries like:

* Telecom
* Banking
* SaaS

This system helps:

* Identify customers likely to leave
* Reduce churn through early intervention
* Improve revenue and retention strategies

---

## 🧩 System Architecture

```
User Input (Streamlit Form)
        ↓
FastAPI Backend (Validation + Logic)
        ↓
PostgreSQL Database (Storage)
        ↓
ML Model (Prediction)
        ↓
Store Prediction
        ↓
Streamlit Dashboard (Visualization)
```

---

## 📁 Project Structure

```
churn_project/
│
├── app/
│   ├── main.py            # FastAPI main application
│   ├── database.py        # Database connection
│   ├── models.py          # Database tables
│   ├── schemas.py         # Pydantic schemas
│   ├── crud.py            # (Optional) DB operations
│   ├── ml/
│   │   ├── model.pkl      # Trained ML model
│   │   ├── predict.py     # Prediction logic
│
├── dashboard/
│   └── app.py             # Streamlit dashboard
│
├── training/
│   └── train_model.py     # Model training script
│
├── .env                   # Environment variables
├── requirements.txt       # Dependencies
└── README.md              # Documentation
```

---

## 🗄 Database Schema

### Table: `customers`

| Column           | Type    |
| ---------------- | ------- |
| id               | Integer |
| gender           | String  |
| SeniorCitizen    | Integer |
| Partner          | String  |
| Dependents       | String  |
| tenure           | Integer |
| PhoneService     | String  |
| MultipleLines    | String  |
| InternetService  | String  |
| OnlineSecurity   | String  |
| OnlineBackup     | String  |
| DeviceProtection | String  |
| TechSupport      | String  |
| StreamingTV      | String  |
| StreamingMovies  | String  |
| Contract         | String  |
| PaperlessBilling | String  |
| PaymentMethod    | String  |
| MonthlyCharges   | Float   |
| TotalCharges     | Float   |

---

### Table: `predictions`

| Column      | Type     |
| ----------- | -------- |
| id          | Integer  |
| customer_id | Integer  |
| prediction  | String   |
| probability | Float    |
| timestamp   | DateTime |

---

## ⚙️ Backend (FastAPI)

### Key Features

* Input validation using Pydantic
* Automatic prediction on data insert/update
* REST APIs for dashboard integration

---

### 🔗 API Endpoints

#### 1. Add Customer

```
POST /customers
```

#### 2. Update Customer

```
PUT /customers/{id}
```

#### 3. Get All Customers

```
GET /customers
```

#### 4. Get Customer by ID

```
GET /customers/{id}
```

#### 5. Dashboard Data

```
GET /dashboard
```

---

## 🤖 Machine Learning Model

### Algorithm Used

* Random Forest Classifier

### Why Random Forest?

* Handles categorical + numerical data
* Robust and less prone to overfitting
* Good performance without heavy tuning

---

### 📊 Evaluation Metrics

* Accuracy
* Precision
* Recall
* Confusion Matrix

👉 **Recall is important** because missing a churn customer means losing revenue.

---

### 🔁 Prediction Pipeline

```
Input Data
   ↓
Preprocessing (Scaling + Encoding)
   ↓
Model Prediction
   ↓
Probability Score
   ↓
Store in Database
```

---

## 📊 Streamlit Dashboard

### Features

* 📌 Total Customers
* 📌 Churn Percentage
* 📌 Average Monthly Charges
* 📊 Churn Distribution Graph
* 📈 Monthly Charges Trend
* 🔥 High-Risk Customers (Probability > 0.7)
* 🔍 Search Customer by ID
* ➕ Add Customer Form
* ✏️ Update Customer Form

---

## ⚡ Real-Time Behavior

* Dashboard auto-refreshes
* New data reflects instantly
* Predictions update dynamically

---

## 🔧 Setup Instructions

### 1️⃣ Clone Project

```
git clone <your-repo-link>
cd churn_project
```

---

### 2️⃣ Install Dependencies

```
pip install -r requirements.txt
```

---

### 3️⃣ Setup PostgreSQL

* Create database:

```
CREATE DATABASE churn_db;
```

* Update `.env` file:

```
DATABASE_URL=postgresql://postgres:password@localhost/churn_db
```

---

### 4️⃣ Train Model

```
python training/train_model.py
```

---

### 5️⃣ Run Backend

```
uvicorn app.main:app --reload
```

---

### 6️⃣ Run Dashboard

```
streamlit run dashboard/app.py
```

---

## 🧪 Testing

* Add customer → prediction generated
* Update customer → prediction changes
* Dashboard updates automatically
* Invalid input handled properly

---

## 💡 Bonus Features (Optional)

* Feature importance visualization
* Risk scoring (Low / Medium / High)
* Filtering customers
* Export data to CSV
* Authentication system

---

## 🧠 Learning Outcomes

After completing this project, you will understand:

* ML model deployment
* API and ML integration
* Real-time data pipelines
* Dashboard visualization
* System design for AI applications

---

## ⚡ Future Improvements

* Deploy on cloud (Render / Railway)
* Add authentication (JWT)
* Use WebSockets for real-time updates
* Improve UI/UX

---

## 🙌 Conclusion

This project demonstrates how machine learning models are used in real-world production systems. It combines backend development, data science, and frontend visualization into a unified solution.

---

## 👨‍💻 Author

**Rehan**
AI / ML Enthusiast 🚀
