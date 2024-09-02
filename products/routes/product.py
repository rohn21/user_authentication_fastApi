from fastapi import APIRouter, HTTPException, Request
from products.models import ProductModel
from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi.responses import JSONResponse
from bson import ObjectId

router = APIRouter()

@router.post("/add-product", response_description="Add a product", response_model=ProductModel)
async def CreateProduct(request: Request, product: ProductModel):
    db:AsyncIOMotorDatabase = request.app.database
    
    try:
        user_id = product.user_id
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid user_id format: {e}")
    
    user = await db["user"].find_one({"_id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not exist.")
    
    product_data = {
        "_id": str(ObjectId()),
        "user_id": user_id,
        "product_name": product.product_name,
        "quantity": product.quantity
    }
    result = await db["products"].insert_one(product_data)
    product_data["_id"] = str(product_data["_id"])
    return JSONResponse({"message": "Product added successfully", "product": product_data})

@router.get("/get-user-product/{user_id}", response_description="Get a product with user info")
async def getUserproduct(request: Request, user_id: str):
    db = request.app.database
    
    user_product = [
        {
            "$match": {
                "user_id": user_id
            }   
        },
        
        {
            "$lookup": {
                "from" : "user",
                "localField": "user_id",
                "foreignField": "_id",
                "as": "user_info"
            }
        },
        
        {
            "$unwind": "$user_info"
        },
        
        {
            "$project": {
                "_id": 1,
                "product_name": 1,
                "quantity": 1,
                "user_info.username": 1,
                "user_info.email": 1                
            }
        }
    ]
    
    output = await db["products"].aggregate(user_product).to_list(length=None)
    
    if not output:
        raise HTTPException(status_code=404, detail="No product found for this user")
    return output

@router.delete("/delete-product/{product_id}", response_description="Delete a product.")
async def deleteProduct(request: Request, product_id: str):
    db = request.app.database
    
    delete_product = await db["products"].find_one({"_id": product_id})    
    if not delete_product:
        raise HTTPException(status_code=404, detail="No product found or wrong product id")
    
    user_id = delete_product["user_id"]
    user_product = await db["user"].find_one({"_id": user_id})
    if not user_product:
        raise HTTPException(status_code=404, detail="No found")    
    
    await db["products"].delete_one({"_id": product_id})
    
    return JSONResponse(content={"message": f"Product delete successfully for {user_product['username']}"})
        
    