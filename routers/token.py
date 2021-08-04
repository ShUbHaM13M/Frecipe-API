from typing import Dict, Optional
from fastapi import APIRouter, Request, Response
from fastapi.params import Header
from fastapi.security.utils import get_authorization_scheme_param
from utils.databaseManager import Database
from utils import mailer
import secrets
import datetime

db = Database.db
router = APIRouter()

def validate_email(email: str) -> bool:
	import re
	regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
	if (re.match(regex, email)):
		return True
	return False


async def already_registered(email: str) -> bool:
	result = await db['registered_consumers'].find_one({'email': email})
	if result:
		return True
	return False

async def validate_token(token: str) -> bool:
	result = await db['registered_consumers'].find_one({'token': token})
	if result:
		return True
	return False

@router.post('/register', include_in_schema=False)
async def send_token(request: Request):

	data = await request.json()
	email = data['email']

	if validate_email(email):

		# TODOs :~
		# CSS layout fix

		if await already_registered(email):
			return {
				'type': 'error',
				'message': 'Entered email is already registered <br> check Your mail for the token'
			}

		token = secrets.token_urlsafe(16)
		await db['registered_consumers'].insert_one({
			'email': email,
			'token': token,
		})

		mailer.send_mail(
			sender_email='shubham.heeralal@gmail.com', 
			recipient=email,
			mail={
				'Subject': 'mail test',
				'text': f'Your API Token: {token}',
				'html': f'Your API Token: {token}'
			})
		return {
			'type': 'success', 
			'message': f'Sent a mail with the API Token to {email}'
			}
	return {
		'type': 'error', 
		'message': 'Enter a valid email address :/'
	}

async def is_authorized(authorization: Optional[str] = Header(...)) -> Dict[str, str]:
	scheme, token = get_authorization_scheme_param(authorization)
	if scheme.lower() != 'token':
		return {
			'type': 'Error', 
			'message': 'No Token provided'
		}
	if await validate_token(token):
		return {
			'type': 'Success', 
			'message': 'Authorized'
		}
	return {
		'type': 'Error', 
		'message': 'Invalid Token provided'
	}

async def update_header(response: Response):
	pass