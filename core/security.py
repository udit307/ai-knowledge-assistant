from fastapi import Header, HTTPException
from core.config import API_TOKEN


def verify_token(x_api_token: str = Header(None)):

    if x_api_token != API_TOKEN:

        raise HTTPException(
            status_code=401,
            detail="Unauthorized"
        )