from pydantic import BaseModel, Field
from bson import ObjectId
from typing import ClassVar


class ProductModel(BaseModel):
    user_id: str
    product_name: str
    quantity: int
    
    class config:
        orm_mode = True
        json_encoders = {
            ObjectId: str
        }
