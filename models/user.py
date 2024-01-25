from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    user_id: Optional[int]
    name: str
    email: str
