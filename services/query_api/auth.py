from jose import JWTError, jwt
from shared.config import settings
from datetime import timedelta
from fastapi import HTTPException, status
from datetime import datetime, timezone

def verify_tenant_jwt(token: str) -> dict:
    """
    Verifies the JWT token and extracts tenant information.
    
    Args:
        token (str): The JWT token to verify.
    
    Returns:
        dict: The decoded token containing tenant information.
    """

    try:
        payload = jwt.decode(token, settings.JWT_SECRET,algorithms=["HS256"])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
def create_tenant_jwt(tenant_id: str, config: dict) -> str:
    """
    Creates a JWT token for the given tenant ID and configuration.
    
    Args:
        tenant_id (str): The tenant ID to include in the token.
        config (dict): Additional configuration to include in the token.
    
    Returns:
        str: The generated JWT token.
    """
    payload = {
        "tenant_id": tenant_id,
        "config": config,
        "exp": datetime.now(timezone.utc) + timedelta(hours=24)  # Token expires in 24 hours
    }
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")
    return token       