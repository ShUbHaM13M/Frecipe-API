from fastapi.exceptions import HTTPException
from routers.token import is_authorized
from fastapi import APIRouter, Request, Header, status
from models.recipe_model import RecipeModel
from typing import Dict, List, Optional
from utils.databaseManager import Database
from utils.rate_limiter import limiter

router = APIRouter()
db = Database.db

@router.get('/', 
	response_description="Get a list of recipes", 
	response_model=Dict[str, List[RecipeModel]],
	tags=['Fetch Recipes']
)
@limiter.limit('5/minute')
async def get_recipes (
	request: Request,
	skip: int = 0, 
	limit: int = 10, 
	authorization: Optional[str] = Header(...),
):
	
	"""*Authorization required in the Header \n
	example: Authorization: Token {Your_Token}. \n\n
	You can have pagination by using the query parameters 'limit' and 'skip'."""
	authorized = await is_authorized(authorization)
	if authorized['type'] == 'Success':
		recipes = await db['recipes'].find().skip(skip).limit(limit).to_list(limit)
		return {"recipes": recipes}
	raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=authorized['message'])

@router.get('/{slug}', 
	response_description="Get a recipe by slug/name", 
	response_model=RecipeModel,
	tags=['Fetch Recipes'],
)
@limiter.limit('5/minute')
async def get_recipe_by_slug (
	request: Request,
	slug: str, 
	authorization: Optional[str] = Header(...)
):

	"""*Authorization required in the Header \n
	example: Authorization: Token {Your_Token}"""	

	authorized = await is_authorized(authorization)
	if authorized['type'] == 'Success':
		if (recipe := await db['recipes'].find_one({"slug": slug})) is not None:
			return recipe
		raise HTTPException(status_code=404, detail=f"{slug}: recipe was not found")
	raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=authorized['message'])