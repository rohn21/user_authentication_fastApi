from fastapi import APIRouter, HTTPException, Request
from products.models import ProductModel
from fastapi.responses import JSONResponse
from bson import ObjectId

router = APIRouter()

@router.post("/add-product", response_description="Add a product", response_model=ProductModel)
async def CreateProduct(request: Request, product: ProductModel):
    """
    Create product with the following details:
    - **user_id**: The id of the user
    - **product_name**: The name of the product
    - **quantity**: The quantity of the product
    - return= product will create that associated with user link with user_id
    """
    
    db = request.app.database
    
    try:
        user_id = product.user_id
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid user_id format: {e}")
    
    user = await db["user"].find_one({"_id": user_id})
    
    if not user:
        raise HTTPException(status_code=404, detail="User not exist.")
    
    product_data = {
        "_id": str(ObjectId()),         # will generate product_id in creation of product
        "user_id": user_id,
        "product_name": product.product_name,
        "quantity": product.quantity
    }
    result = await db["products"].insert_one(product_data)
    product_data["_id"] = str(product_data["_id"])
    return JSONResponse({"message": "Product added successfully", "product": product_data})

@router.get("/get-user-product/{user_id}", response_description="Get a product with user info")
async def getUserproduct(request: Request, user_id: str):
    """
    Fetch a product and associated user using filter method of aggregate:
    - **user_id**: The id of the user
    - return= the product and associated user info will return. 
    """
    
    db = request.app.database
    
    # 
    user_product = [
        # $match: to match/linked data using user_id  
        {
            "$match": {
                "user_id": user_id
            }   
        },
        # $lookup: find the linked collection for associated data, e.g. 'user' collection
        {
            "$lookup": {
                "from" : "user",
                "localField": "user_id",
                "foreignField": "_id",
                "as": "user_info"
            }
        },
        
        # $unwind: filter element within an array
        {
            "$unwind": "$user_info"
        },
        
        # $project: include/exclude field, create new field based on existing fields, 
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
    """
    Delete a product with the following details:
    - **product_id**: The id of the product
    - return= only the product will delete and returns name of associated user. 
    """
    
    db = request.app.database
    
    delete_product = await db["products"].find_one({"_id": product_id})    
    if not delete_product:
        raise HTTPException(status_code=404, detail="No product found or wrong product id")
    
    #to find username using user_id that associated with that product 
    user_id = delete_product["user_id"]
    user_product = await db["user"].find_one({"_id": user_id})
    if not user_product:
        raise HTTPException(status_code=404, detail="Not found")    
    
    await db["products"].delete_one({"_id": product_id})    #delete_one : only delete the requested data 
    
    return JSONResponse(content={"message": f"Product delete successfully for {user_product['username']}"})