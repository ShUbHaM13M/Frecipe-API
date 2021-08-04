import motor.motor_asyncio
from config import Settings

settings = Settings()

class Database:
	client = motor.motor_asyncio.AsyncIOMotorClient(settings.DATABASE_URI)
	db = client.RecipeApp

