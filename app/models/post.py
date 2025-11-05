from pydantic import BaseModel, Field, GetJsonSchemaHandler
from typing import Optional, Any
from bson import ObjectId
from typing import Annotated
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema


class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, source, handler):
        return core_schema.no_info_before_validator_function(
            cls.validate,
            core_schema.str_schema()
        )

    @classmethod
    def validate(cls, v: Any) -> ObjectId:
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)
    

    @classmethod
    def __get_pydantic_json_schema__(
        cls, 
        schema: JsonSchemaValue, 
        handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        return {"type": "string"}


class PostCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, description="文章标题")
    content: str = Field(..., min_length=5, description="文章内容")


class PostInDB(BaseModel):
    _id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title: str
    content: str
    author_id: str

    model_config = {
        "populate_by_name": True,
        "json_encoders": {ObjectId: str}
    }