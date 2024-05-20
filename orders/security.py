from jose import jwt
from config import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"

# Function to verify the jwt token provided by user during login
def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            return None
        return user_id
    except jwt.JWTError:
        return None