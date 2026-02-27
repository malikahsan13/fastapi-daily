from fastapi import FastAPI
from typing import List
from pydantic import BaseModel

app = FastAPI()

class Address(BaseModel):
    street: str
    city: str
    zip_code: str
    
class Person(BaseModel):
    name: str
    age: int
    address: Address
    
class Company(BaseModel):
    name: str
    employee: List[Person]
    
@app.post("/company/", response_model=Company)
async def create_company(company: Company):
    return company