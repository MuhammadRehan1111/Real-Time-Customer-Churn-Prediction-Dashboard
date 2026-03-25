from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import SessionLocal, engine, Base
from app.models import Customer, Prediction
from app.schemas import CustomerCreate
from app.ml.predict import predict_customer

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ADD CUSTOMER
@app.post("/customers")
def add_customer(data: CustomerCreate, db: Session = Depends(get_db)):

    customer = Customer(**data.dict())
    db.add(customer)
    db.commit()
    db.refresh(customer)

    result = predict_customer(data.dict())

    prediction = Prediction(
        customer_id=customer.id,
        prediction=result["prediction"],
        probability=result["probability"]
    )

    db.add(prediction)
    db.commit()

    return {"id": customer.id, "prediction": result}

# UPDATE CUSTOMER
@app.put("/customers/{id}")
def update_customer(id: int, data: CustomerCreate, db: Session = Depends(get_db)):

    customer = db.query(Customer).filter(Customer.id == id).first()

    for key, value in data.dict().items():
        setattr(customer, key, value)

    db.commit()

    result = predict_customer(data.dict())

    db.query(Prediction).filter(Prediction.customer_id == id).delete()

    new_pred = Prediction(
        customer_id=id,
        prediction=result["prediction"],
        probability=result["probability"]
    )

    db.add(new_pred)
    db.commit()

    return result

# GET CUSTOMERS
@app.get("/customers")
def get_customers(db: Session = Depends(get_db)):

    customers = db.query(Customer).all()
    results = []

    for c in customers:
        pred = db.query(Prediction).filter(Prediction.customer_id == c.id).first()

        results.append({
            "id": c.id,
            "gender": c.gender,
            "tenure": c.tenure,
            "MonthlyCharges": c.MonthlyCharges,
            "Contract": c.Contract,
            "prediction": pred.prediction if pred else None,
            "probability": pred.probability if pred else None
        })

    return results

# DASHBOARD
@app.get("/dashboard")
def dashboard(db: Session = Depends(get_db)):

    total = db.query(Customer).count()

    churn = db.query(Prediction).filter(Prediction.prediction == "Yes").count()

    avg = db.query(func.avg(Customer.MonthlyCharges)).scalar()

    return {
        "total_customers": total,
        "churn_percentage": (churn / total) * 100 if total else 0,
        "avg_monthly_charges": avg
    }

@app.get("/customers/{customer_id}")
def get_customer(customer_id: int, db: Session = Depends(get_db)):

    c = db.query(Customer).filter(Customer.id == customer_id).first()

    if not c:
        return {"error": "Customer not found"}

    pred = db.query(Prediction).filter(Prediction.customer_id == c.id).first()

    return {
        "id": c.id,
        "gender": c.gender,
        "tenure": c.tenure,
        "MonthlyCharges": c.MonthlyCharges,
        "Contract": c.Contract,
        "prediction": pred.prediction if pred else None,
        "probability": pred.probability if pred else None
    }