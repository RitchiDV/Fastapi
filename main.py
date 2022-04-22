#python____librerias______
#
from email import message
from enum import Enum#
from typing import Optional
from unittest.util import _MAX_LENGTH#
#_pydantic________________
from pydantic import PaymentCardNumber#es para crear un icomers pide el numero de la targeta de credito
from pydantic import EmailStr#validacion de email
from pydantic import BaseModel#libreria para modelos u objetos 
from pydantic import Field#validacion de los atributos en las clases
#fastAPI___________________
from fastapi import FastAPI, Form, Header, Cookie #(form : indica que un paramtro dentro de una path= <- viene de un formulario )
from fastapi import status#status code personalisados
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
        max_length=50,
        example= "manzanillo"
    )
    state:str = Field(
        ...,
        min_length=1,
        max_length=50,
        example= "colima"
    )
    country:str = Field(
        ...,
        min_length=1,
        max_length=50,
        example= "las torres"
    )



class personbase(BaseModel):#erencia  de person base para no repetir lineas
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        example= "Ricardo"
        
    )
    last_name:str= Field(
        ...,
        min_length=1,
        max_length=50,
        example = "diaz"
    )    
    age: int = Field(
        ...,
        gt=0,
        le=100
    )    
    hair_color:Optional[haircolor]= Field(default=None)

    is_married:Optional[bool]= Field(default=None)

    email:Optional[emaill]= Field(default=None) # validacion de email




#models _ modelos (person)
class person(personbase):
    password: str = Field(
        ...,
        min_length=8,
        max_length=20
    )
    # card = Card(
    # card_numbers="4000000000000002")


class personOut(personbase):#personOut contiene lo de personbase 
    pass

class loginOut(BaseModel):
    username:str = Field(
        ...,
        max_length=20,
        example ="richard2021"
        )
    message: str = Field(default="login succesfully!")


@app.get(
    path="/",
    status_code=status.HTTP_200_OK)#status code personalisados
def home():
    return{"hello":"world"}


#_________request and response  body_______________________________________
@app.post(
    path="/person/new",
    response_model=personOut,#entra por person y al mandar la respuesta al cliente se manda personOut como respuesta.
    status_code=status.HTTP_201_CREATED
)
def create_person(person: person = Body(...)):# se creea un modelo de la class person y se representa en (def con person )
    return person

#_____Validaciones: Query Parameters_______________________________________
@app.get(
    path="/person/detail",
    status_code=status.HTTP_200_OK
    )
def show_person(
    name:Optional[str] =Query(
        None,
        min_length=1,
        max_length=50,
        title = "person name",
        description = "this is the person . it's between 1 and 50  characters",
        example ="ricardo"
    ),
    age:str= Query(
        ...,
        title="person age",
        description="this is the person age. is's required",
        example = "23"
    )
):
    return{name:age}

    
#______validaciones path parameters___{person_id}______________________________________

@app.get(
    path="/person/detail/{person_id}",
    status_code=status.HTTP_200_OK
    )
def show_person(
    person_id: int = Path(
        ...,
        title="person id",
        description="this is the person id . it's  required",
        gt=0,
        example=123 )
):

    return{person_id: "it exists!!"}


# validaciones : request Body

@app.put(
    path="/person/{person_id}",
    status_code=status.HTTP_200_OK
    )
def update_person(
    person_id: int = Path(
        ...,# los 3 puntos es que el parametro  patch es obligatorio
        title="person ID",
        description ="this is the person ID",
        gt=0,
        example=123# < gt = mayor que 0
    ),
    person:person = Body(...),
    location:location = Body(...) # se creo una clase para location y su libreria Basemodel
):
    #creando dos request body 
    results = person.dict()#comvertimos el request en dictcionario
    results.update(location.dict())#combinamos person con location con .update
    return results#result se le asigna el valor y se retorna 


@app.post(
    path="/login",
    response_model=loginOut,
    status_code=status.HTTP_200_OK
)
def login (username: str=Form(...), password: str = Form(...)):
    return loginOut(username=username)

#cookies and headers parameters
@app.post(
   path="/conntact",
   status_code=status.HTTP_200_OK
)
def contact (
    firts_name: str = Form(
        ...,
        max_length=20,
        min_length=1
     
    ),
    last_name: str = Form(
        ...,
        max_length=20,
        min_length=1
    
    ),
    email: EmailStr = Form(...),
    messaje:str = Form(
        ...,
        min_length=20   
    ),
    user_agent: Optional[str]= Header(default=None),
    ads: Optional[str]=Cookie(default=None)



):
    return user_agent

