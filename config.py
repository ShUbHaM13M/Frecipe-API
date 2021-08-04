from pydantic import BaseSettings

class Settings(BaseSettings):
	APP_NAME: str
	DATABASE_URI: str
	DATABASE_PASS: str
	DATABASE_USER: str
	COLLECTION: str
	MAIL_PASS: str
	MAIL_ACCOUNT: str
	SMTP_CLIENT: str

	class Config:
		env_file = '.env'