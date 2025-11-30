from pydantic import BaseModel

class TokenRefreshRequest(BaseModel):
    refresh_token: str

class TokenPair(BaseModel):
    access_token: str
    token_type: str = "bearer"
    refresh_token: str
    expires_in: int