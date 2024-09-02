from fastapi import APIRouter, HTTPException, status, Request, Body
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from user_auth.models import UserModel, UserCreateModel, UserLoginModel, LinkIdModel
from user_auth.utils.pwd_hash import pass_hash, verify_password
from typing import List
# from motor.motor_asyncio import AsyncIOMotorDatabase

router = APIRouter()  

#request endpoint for User registration
@router.post("/register", response_description="Register a new user", status_code=status.HTTP_201_CREATED, response_model=UserModel)
async def registerUser(request: Request, user: UserCreateModel = Body(...)):
    """
    Register a new user with the following details:
    - **username**: The name of the user
    - **email**: The email of the user
    - **password**: The password of the user
    """
    
    db = request.app.database
    
    user_exist = await db["user"].find_one({"email": user.email})
    if user_exist:
        raise HTTPException(status_code=400, detail="Email already exist.")
    
    hashed_password = pass_hash(user.password) #imported from utils/pwd_hash - pass_hash
    new_user = UserModel(username=user.username, email=user.email, password=hashed_password, linked_id="")
    
    new_user = jsonable_encoder(new_user) #convert an object into encoded JSON format
    new_user_data = await db["user"].insert_one(new_user)
    created_user_data = await db["user"].find_one({"_id": new_user_data.inserted_id})
    
    return UserModel(**created_user_data)  

@router.post("/login", response_description="User Login", response_model=UserModel)
async def UserLogin(request: Request, user: UserLoginModel = Body(...)):
    """
    User login with the following details:
    - **email**: The email of the user
    - **password**: The password of the user
    """
    
    db = request.app.database
    
    user_data = await db["user"].find_one({"email": user.email})
    
    #exception handling with email and password verification
    if not user_data:
        raise HTTPException(status_code=400, detail="Email or found")
    
    if not verify_password(user.password, user_data["password"]):
        raise HTTPException(status_code=400, detail="Incorrect password")
    
    user_model = UserModel(**user_data)
    user_return = jsonable_encoder(user_model)
    
    return JSONResponse({"message": "Login Successful", "user": user_return})

@router.post("/link-id", response_description="Link an ID to user", response_model=UserModel)
async def LinkUserId(request: Request, link_info: LinkIdModel = Body(...)):
    """
    Lining an ID to user with the following details:
    - **email**: The email of the user
    - **link_id**: The ID want to link
    e.g. can be a Subscription Id, Membership Id
    """
    
    db = request.app.database
    
    user_data = await db["user"].find_one({"email": link_info.email})
    if not user_data:
        raise HTTPException(status_code=400, detail="Email or found")
    
    update_result = await db["user"].update_one(                    #to update single document uses update_one
        {"email": link_info.email}, {"$set": {"linked_id": link_info.linked_id}}
    )
    
    #it will check that how many times the document was updated, if it failed to update will raise an error
    if update_result.modified_count == 0:
        raise HTTPException(status_code=500, detail="Failed to link")
    
    update_user_info = await db["user"].find_one({"_id": user_data["_id"]})
    if not update_user_info:
        raise HTTPException(status_code=500, detail="Failed to retrieve data")
    
    user_model = UserModel(**update_user_info)
    user_return = jsonable_encoder(user_model)
    
    return JSONResponse({"message": "ID linked successfully", "user": user_return})

@router.delete("/remove-user/{user_id}", response_description="Remove user and associated data")
async def removeUser(request: Request, user_id: str):
    """
    Removes an user and associated data with them using following details:
    - **user_id**: request user_id as parameter in request_url
    """
    db = request.app.database
    
    user_data = await db["user"].delete_one({"_id": user_id})
    
    if user_data.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    
    product_data = await db["products"].delete_many({"user_id": user_id})
    
    return {"message": "Remove record successfully"}

@router.get("/get-data", response_description="Get all Data", response_model=List[UserModel])
async def getAllUsers(request: Request):
    """
    Simple API to get all user data from 'user' collection:
    - will return user_data list in JSON format
    """
    
    db = request.app.database
    
    users = await db["user"].find().to_list(500)
    
    for data in users:
        data["id"] = str(data["_id"])
        
    user_model = [UserModel(**data) for data in users]
    return JSONResponse(content=jsonable_encoder(user_model)) 

@router.get("/get-user-data/{user_id}", response_description="Get user Data", response_model=UserModel)
async def getUserData(request: Request, user_id: str):
    """
    Return specific user data from 'user' collection:
    - "user_id": request user_id for the user data as parameter in request_url
    """
    
    db = request.app.database
    
    user = await db["user"].find_one({"_id": user_id})
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    
    user_product = await db["products"].count_documents({"user_id": user_id, "quantity": {"$gt": 0}})
    user["has_product"] = user_product > 0
    
    user["_id"] = str(user["_id"])
    return JSONResponse(content=jsonable_encoder(user))
