from fastapi import FastAPI, HTTPException
from dotenv import dotenv_values, load_dotenv
import motor.motor_asyncio, os
from user_auth.routes import user as user_routes
from products.routes import product as product_routes

# config = dotenv_values("../.env")
load_dotenv()

# for better API documentation  visit - http://127.0.0.1:8000/redoc to understand better
app = FastAPI(
    title="User Authentication and CRUD operations",
    description="This is a simple FastAPI project user registration and product management functionalities using MongoDB.",
    version="1.0.0"
)

@app.get("/")
async def read_root():
    return {"message": "API using Fast API and pymongo"}

@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("MONGODB_CONNECTION_URI"))
    app.database = app.mongodb_client[os.getenv("DB_NAME")]
    print("Connected to the MongoDB database!")
    
@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()

#will check the database connection
"""@app.get("/check_db_connection")
async def check_db_connection():
    try:
        # Attempt to list collections to check the connection
        collections = await app.database.list_collection_names()
        return {"message": "Database connected successfully!", "collections": collections}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Database connection failed")"""
    

#handling router for both app

#user_router
app.include_router(user_routes.router, prefix="/users", tags=["users"])  

#products_router
app.include_router(product_routes.router, prefix="/products", tags=["products"])  