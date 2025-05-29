from pydantic import BaseModel


class Token(BaseModel):
    """Токен."""

    access_token: str
    token_type: str


class TokenRefresh(BaseModel):
    """Токен обновления."""

    refresh_token: str
