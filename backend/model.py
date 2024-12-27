from pydantic import BaseModel, Field
from bson import ObjectId
from datetime import datetime
from typing import Optional


# Helper function to handle ObjectId serialization
def str_to_objectid(id: str) -> ObjectId:
    return ObjectId(id) if id else None


class Trend(BaseModel):
    _id: ObjectId  # Make _id a required field
    nameOfTrend1: Optional[str] = None
    nameOfTrend2: Optional[str] = None
    nameOfTrend3: Optional[str] = None
    nameOfTrend4: Optional[str] = None
    date_time_of_end: datetime
    ip_address: str

    class Config:
        # This will make Pydantic parse ObjectId as str
        json_encoders = {ObjectId: str}

    # Method to convert a MongoDB document to a Pydantic model
    @classmethod
    def from_mongo(cls, data):
        # Make sure _id is correctly converted to string
        data["_id"] = str(data["_id"])
        return cls(**data)
