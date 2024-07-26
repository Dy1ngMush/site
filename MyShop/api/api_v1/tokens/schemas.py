from pydantic import BaseModel
from uuid import UUID


class Token(BaseModel):
    access_token: str


class TokenRead(Token):
    id: UUID
