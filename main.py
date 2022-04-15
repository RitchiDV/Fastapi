#python____librerias______
from typing import Optional
#_pydantic________________
from pydantic import BaseModel
#fastAPI___________________
from fastapi import FastAPI
from fastapi import Body

app = FastAPI()

#models _ modelos
class person(BaseModel):
    first_name: str
    last_name:str
    age: int
    hair_color:Optional[str]= None
    is_married:Optional[bool]= None


@app.get("/")
def home():
    return{"hello":"world"}

    
#_________request and response  body_______________________________________
@app.post("/person/new")
def create_person(person: person = Body(...)):
    return person