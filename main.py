from typing import Optional
from slowapi.errors import RateLimitExceeded
import uvicorn
from fastapi import FastAPI, Request, Header
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from routers import fetch_recipe, token, modify_recipe
from utils.rate_limiter import limiter
from slowapi import _rate_limit_exceeded_handler

app = FastAPI(
	title="Frecipe - Free recipe API",
	description="""
	Frecipe API is a free API to get recipes.
	currently it serves 9500+ recipes,
	with more being added ocassionaly (^^)

	**Rate Limit: 5 requests per minute.""",
	contact={"name": "Shubham Maurya", "email": "shubham.heeralal@gmail.com"}
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(fetch_recipe, prefix="/api/recipes")
app.include_router(token, prefix="/api")
app.include_router(modify_recipe, prefix="/admin/modify")
app.mount('/static', StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="static/")

@app.get('/', include_in_schema=False)
async def index(request: Request):
	return templates.TemplateResponse("index.html", {"request": request})

if __name__ == "__main__":
	uvicorn.run("main:app", port=8000, host='127.0.0.1')