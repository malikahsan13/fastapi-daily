from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    username: Optional[str] = None
    
class UserCreate(BaseModel): 
    username: str
    email: str
    full_name: Optional[str] = None
    password: str
    
class User(BaseModel):
    id: Optional[int]
    username: str
    email: str
    full_name: Optional[str] = None
    disabled: Optional[bool] = False
    
    class Config:
        orm_mode = True
    