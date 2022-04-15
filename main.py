#python____librerias______
from typing import Optional
#_pydantic________________
from pydantic import BaseModel
#fastAPI___________________
from fastapi import FastAPI, Query
from fastapi import Body#validacion obligatoria
from fastapi import Query# validaciones Opcionales en parametros

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
def create_person(person: person = Body(...)):# se creea un modelo de la class person y se representa en (def con person )
    return person


#_____Validaciones: Query Parameters_______________________________________
@app.get("/person/detail")
def show_person(
    name:Optional[str] =Query (None, min_length=1,max_length=50),
    age : str = Query(...)
):
    return{name:age}