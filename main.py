#python____librerias______
#
from enum import Enum#
from typing import Optional#
#_pydantic________________
from pydantic import PaymentCardNumber#es para crear un icomers pide el numero de la targeta de credito
from pydantic import EmailStr#validacion de email
from pydantic import BaseModel#libreria para modelos u objetos 
from pydantic import Field#validacion de los atributos en las clases
#fastAPI___________________
from fastapi import FastAPI #
from fastapi import Body#validacion obligatoria
from fastapi import Query# validaciones Opcionales en parametros
from fastapi import Path#con esto definimos las path parameter
app = FastAPI()



class Card(PaymentCardNumber):
    card_numbers = PaymentCardNumber

class emaill(EmailStr):#validacion de email
    example = "@gmail.com"


class haircolor(Enum):
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"


#modelos (location)
class location(BaseModel):
    city:str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    state:str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    country:str = Field(
        ...,
        min_length=1,
        max_length=50
    )



#models _ modelos (person)
class person(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=100
        
    )
    last_name:str= Field(
        ...,
        min_length=1,
        max_length=50
    )    
    age: int = Field(
        ...,
        gt=0,
        le=100
    )    
    hair_color:Optional[haircolor]= Field(default=None)

    is_married:Optional[bool]= Field(default=None)

    email:Optional[emaill]= Field(default=None) # validacion de email

    card_numbers: int = Field(
        ...,
        gt=0,
        lt=18
    )
    # card = Card(
    # card_numbers="4000000000000002")
    
    


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
    name:Optional[str] =Query (
        None,
        min_length=1,
        max_length=50,
        title = "person name",
        description = "this is the person . it's between 1 and 50  characters"
    ),
    age : str= Query(
        ...,
        title="person age",
        description="this is the person age. is's required"
        )
):
    return{name:age}

    
#______validaciones path parameters___{person_id}______________________________________

@app.get("/person/detail/{person_id}")
def show_person(
    person_id: int = Path(
        ...,
        title="person id",
        description="this is the person id . it's  required",
         gt=0)
):
    return{person_id: "it exists!!"}


# validaciones : request Body

@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(
        ...,# los 3 puntos es que el parametro  patch es obligatorio
        title="person ID",
        description ="this is the person ID",
        gt=0# < gt = mayor que 0
    ),
    person:person = Body(...),
    location:location = Body(...) # se creo una clase para location y su libreria Basemodel
):
#creando dos request body 
    results = person.dict()#comvertimos el request en dictcionario
    results.update(location.dict())#combinamos person con location con .update
    return results#result se le asigna el valor y se retorna 