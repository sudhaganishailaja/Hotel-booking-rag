from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd

# Load hotel bookings dataset
df = pd.DataFrame({
    "hotel": ["City Hotel", "Resort Hotel", "City Hotel"],
    "arrival_date_year": [2017, 2017, 2017],
    "arrival_date_month": ["July", "July", "July"],
    "adr": [266.2, 184.0, 150.0],  # Average Daily Rate (ADR)
    "is_canceled": [0, 1, 1]
})

app = FastAPI()

# Data Model for requests
class QueryRequest(BaseModel):
    question: str

@app.get("/")
def home():
    return {"message": "🚀 FastAPI is running successfully!"}

@app.post("/analytics")
def get_analytics():
    """Precomputed analytics for hotel bookings."""
    total_revenue = df[df["arrival_date_month"] == "July"]["adr"].sum()
    highest_cancellations = df[df["is_canceled"] == 1]["hotel"].value_counts().idxmax()
    avg_price = df["adr"].mean()

    return {
        "total_revenue_july_2017": total_revenue,
        "highest_cancellation_hotel": highest_cancellations,
        "average_booking_price": avg_price
    }

@app.post("/ask")
def answer_question(query: QueryRequest):
    """Simple Q&A system for hotel bookings."""
    question = query.question.lower()

    if "total revenue" in question and "july 2017" in question:
        return {"answer": f"Total revenue for July 2017 is ${df[df['arrival_date_month'] == 'July']['adr'].sum()}"}
    
    elif "highest booking cancellations" in question:
        return {"answer": f"Hotel with the highest cancellations: {df[df['is_canceled'] == 1]['hotel'].value_counts().idxmax()}"}
    
    elif "average price" in question:
        return {"answer": f"Average hotel booking price is ${df['adr'].mean():.2f}"}
    
    else:
        raise HTTPException(status_code=404, detail="Question not recognized")
