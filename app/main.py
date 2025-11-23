from fastapi import FastAPI
from core import database  # Import the database module

app = FastAPI(title = 'Ecom-framework')

@app.get('/')
def root():
    return{"message":"E-commerce is online"}