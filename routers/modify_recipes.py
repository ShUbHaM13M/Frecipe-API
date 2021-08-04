from fastapi import HTTPException, status, Request
from typing import Dict, List, Optional

from fastapi.encoders import jsonable_encoder
from fastapi.params import Header
from starlette.responses import JSONResponse
from models import RecipeModel, UpdateRecipeModel
from fastapi import APIRouter, Response
from utils.databaseManager import Database
from routers.token import is_authorized, update_header
from utils.rate_limiter import limiter

db = Database.db
router = APIRouter()

def create_slug(from_string: str) -> str:
	return from_string.strip().replace(' ', '-').lower()

@router.post('/', 
	response_description="Create a new recipe", 
	response_model=RecipeModel, 
	include_in_schema=False
)
async def create_recipe(recipe: RecipeModel):
	recipe.slug = create_slug(recipe.title)
	recipe = jsonable_encoder(recipe)
	new_recipe = await db['recipes'].insert_one(recipe)
	created_recipe = await db['recipes'].find_one({"_id": new_recipe.inserted_id})
	return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_recipe)

# adding validation to the recipe post, delete, put endpoints
# Testing this endpoint later
# @router.put('/{id}', 
# 	response_description="Update an existing recipe",
# 	response_model=RecipeModel, 
# 	include_in_schema=True
# )
# async def update_recipe(id: str, recipe: UpdateRecipeModel):
# 	recipe = {k: v for k, v in recipe.dict().items() if v is not None}
# 	if len(recipe) > 1:
# 		update_result = await db['recipes'].update_one({'_id': id}, {"$set": recipe})

# 		if update_result.modified_count == 1:
# 			if (updated_recipe := await db['recipes'].find_one({'_id': id})) is not None:
# 				return updated_recipe
	
# 	if (existing_recipe := await db['recipes'].find_one({'_id': id})) is not None:
# 		return existing_recipe

# 	raise HTTPException(status_code=404, detail=f"Recipe with id: {id} not found")

@router.delete('/{id}', include_in_schema=False)
async def delete_recipe(id: str):
	delete_result = await db['recipes'].delete_one({"_id": id})
	if delete_result.deleted_count == 1:
		return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
	raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Recipe with id: {id} not found")