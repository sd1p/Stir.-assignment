from pydantic import BaseModel, Field
from bson import ObjectId
from datetime import datetime
from typing import Optional, List


def str_to_objectid(id: str) -> ObjectId:
    return ObjectId(id) if id else None


class Trend(BaseModel):
    _id: ObjectId
    trends: List[Optional[str]] = []
    date_time_of_end: datetime
    ip_address: str

    class Config:
        json_encoders = {ObjectId: str}

    @classmethod
    def from_mongo(cls, data):
        data["_id"] = str(data["_id"])
        return cls(**data)
