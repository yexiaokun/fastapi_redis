from pydantic import BaseModel, Field, GetJsonSchemaHandler
from typing import Optional, Any
from bson import ObjectId
from typing import Annotated
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema


class PyObjectId(ObjectId):
    @classmethod
    def validate(cls, v: Any) -> ObjectId:
        if isinstance(v, ObjectId):  # 如果已经是 ObjectId，直接返回
            return v
        if isinstance(v, str):       # 如果是字符串，验证并转换
            if ObjectId.is_valid(v):
                return ObjectId(v)
            else:
                raise ValueError("Invalid ObjectId string")
        raise ValueError("Invalid ObjectId")

    @classmethod
    def __get_pydantic_core_schema__(cls, source, handler):
        return core_schema.no_info_before_validator_function(
            cls.validate,
            core_schema.union_schema([  # 允许 str 或 ObjectId
                core_schema.str_schema(),
                core_schema.is_instance_schema(ObjectId)
            ])
        )
    

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
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title: str
    content: str
    author_id: PyObjectId

    model_config = {
        "populate_by_name": True,
        "json_encoders": {ObjectId: str}
    }