from pydantic import BaseModel
from bson import ObjectId

class ProductModel(BaseModel):
    user_id: str
    product_name: str
    quantity: int
    
    class config:
        orm_mode = True
        json_encoders = {
            ObjectId: str
        }