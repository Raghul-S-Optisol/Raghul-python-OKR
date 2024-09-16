# app/config/database.py
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import os
from dotenv import load_dotenv
from pydantic import GetCoreSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic import BaseModel
from pydantic_core import core_schema

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = AsyncIOMotorClient(MONGO_URI)
db = client["Raghul_DataBase"]

# Utility function for converting ObjectId to string in Pydantic v2
class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(
        cls, _source_type: type, handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        return handler(str)

    @classmethod
    def __get_pydantic_json_schema__(
        cls, _core_schema: core_schema.CoreSchema, handler
    ) -> JsonSchemaValue:
        json_schema = handler(_core_schema)
        json_schema.update(type="string")
        return json_schema
