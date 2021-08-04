from typing import Dict, List, Optional
from bson.objectid import ObjectId
from pydantic.fields import Field
from pydantic.main import BaseModel


class PyObjectId(ObjectId):
	@classmethod
	def __get_validators__(cls):
		yield cls.validate
	
	@classmethod
	def validate(cls, v):
		if not ObjectId.is_valid(v):
			raise ValueError('Invalid ObjectId')
		return ObjectId(v)
	
	@classmethod
	def __modify_schema__(cls, field_schema):
		field_schema.update(type="string")


class RecipeModel(BaseModel):
	id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
	title: str = Field(...)
	slug: Optional[str] = Field()
	info: List[Dict[str, str]] = Field(...)
	ingredients: List[str] = Field(...)
	directions: List[str] = Field(...)

	class Config:
		json_encoders = {ObjectId: str}
		schema_extra = {
			"example": {
				"title": "Tequila-Soaked Watermelon Wedges",
				"slug": "tequila-soaked-watermelon-wedges",
				"info": [
					{"header": "prep", "body": '5mins'},
					{"header": "total", "body": '1 hr'},
					{"header": "Servings", "body": '4'}
				],
				"ingredients": [
					"1 small seedless watermelon, red or yellow, quartered and cut into 1-inch-thick wedges",
					"1 cup sugar",
					"3/4 cup water",
					"1/2 cup tequila",
					"1/4 cup Triple Sec",
					"2 limes, halved or cut into wedges",
					"Flaked sea salt or coarse salt"
				],
				"directions": [
					"Arrange watermelon in a single layer in two 9-by-13-inch baking dishes. Bring sugar, water, tequila, and Triple Sec to a boil in a small saucepan. Cook, stirring, until sugar dissolves, about 1 minute. Let cool slightly. Pour syrup over watermelon wedges, and refrigerate for at least 45 minutes.",
					"Remove watermelon from syrup, and arrange on a platter. Squeeze limes over melon, and season with salt."
				]
			}
		}

class UpdateRecipeModel(BaseModel):
	title: Optional[str]
	slug: Optional[str]
	info: Optional[List[Dict[str, str]]]
	ingredients: Optional[List[str]]
	directions: Optional[List[str]]

	class Config:
		arbirary_types_allowed: True
		json_encoders = {ObjectId: str}