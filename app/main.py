from datetime import date
from fastapi import  FastAPI
from fastapi import FastAPI, Query, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from database import SessionLocal,engine
from models import Sales
 

import models

app = FastAPI()

models.Base.metadata.create_all(bind=engine)



# --------------------------------------Endpoints to retrieve, filter, and analyze sales data-----------------------1
# Endpoint sales
# /sales/
@app.get('/sales/')
async def get_sales(

    start_date: str = Query('2023-01-10', description="Start date for filtering"),
    end_date: str = Query('2023-09-27', description="End date for filtering"),
    product_id: int = None,
    
):
    db = SessionLocal()
    try:
        # Build the filter conditions based on the provided parameters
        filter_conditions = [
            models.Sales.sale_date >= start_date,
            models.Sales.sale_date <= end_date,
        ]
        if product_id:
            filter_conditions.append(models.Sales.product_id == product_id)

        # Query the database and apply the filter conditions
        sales_data = db.query(models.Sales).filter(*filter_conditions).all()

        return {"sales": sales_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        db.close()




# --------------------Endpoints to analyze revenue on a daily, weekly, monthly, and annual basis-------------------2
# # Function to calculate revenue for a specific time period
def calculate_revenue(db: Session, start_date, end_date):
    revenue_data = db.query(Sales.sale_date, func.sum(Sales.revenue).label('revenue')).filter(
        Sales.sale_date >= start_date,
        Sales.sale_date <= end_date
    ).group_by(Sales.sale_date).all()
    return revenue_data

# Daily Revenue Analysis Endpoint
# /revenue/daily?start_date=2023-09-27&end_date=2023-10-02
@app.get("/revenue/daily") 
async def get_daily_revenue(start_date: date, end_date: date):
    db = SessionLocal()
    try:
        daily_revenue = calculate_revenue(db, start_date, end_date)
        return {"daily_revenue": daily_revenue}
    finally:
        db.close()

# Weekly Revenue Analysis Endpoint
@app.get("/revenue/weekly")
async def get_weekly_revenue(start_date: date, end_date: date):
    db = SessionLocal()
    try:
        weekly_revenue = calculate_revenue(db, start_date, end_date)
        return {"weekly_revenue": weekly_revenue}
    finally:
        db.close()

# Monthly Revenue Analysis Endpoint
@app.get("/revenue/monthly")
async def get_monthly_revenue(start_date: date, end_date: date):
    db = SessionLocal()
    try:
        monthly_revenue = calculate_revenue(db, start_date, end_date)
        return {"monthly_revenue": monthly_revenue}
    finally:
        db.close()

# Annual Revenue Analysis Endpoint
@app.get("/revenue/annual")
async def get_annual_revenue(start_date: date, end_date: date):
    db = SessionLocal()
    try:
        annual_revenue = calculate_revenue(db, start_date, end_date)
        return {"annual_revenue": annual_revenue}
    finally:
        db.close()





# ---------------------------Provide sales data by date range, product--------------------------4
# Provide sales by date range
@app.get("/sales/by_date/")
def get_sales_by_date_range(start_date: date, end_date: date,db = SessionLocal()):
    sales_data = db.query(Sales).filter(Sales.sale_date >= start_date, Sales.sale_date <= end_date).all()
    return {"sales": sales_data}

# Provide sales by product
@app.get("/sales/by_product/")
def get_sales_by_product(product_id: int,db = SessionLocal()):
    sales_data = db.query(Sales).filter(Sales.product_id == product_id).all()
    return {"sales": sales_data}