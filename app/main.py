from fastapi import FastAPI

app = FastAPI(title = 'Ecom-framework')

@app.get('/')
def root():
    return{"message":"E-commerce is online"}