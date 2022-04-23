#python____librerias______
#
from enum import Enum
from typing import Optional
#_pydantic________________
from pydantic import PaymentCardNumber#es para crear un icomers pide el numero de la targeta de credito
from pydantic import EmailStr#validacion de email
from pydantic import BaseModel#libreria para modelos u objetos 
from pydantic import Field#validacion de los atributos en las clases
#fastAPI___________________
from fastapi import FastAPI, File, Form, Header, Cookie, UploadFile #(form : indica que un paramtro dentro de una path= <- viene de un formulario )
from fastapi import status#status code personalisados
from fastapi import Body#validacion obligatoria
from fastapi import Query# validaciones Opcionales en parametros
from fastapi import Path#con esto definimos las path parameter
from fastapi import UploadFile#{ sintaxis
        #"filename":video.filename,
        #"format":video.content_type,
        #"Size(kb)":round(len(video.file.read())/1024,ndigits=2)
    #}


from fastapi import HTTPException# status_code=status.HTTP_404_NOT_FOUND,
                                 # detail="this person doesn't exists"

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
    status_code=status.HTTP_200_OK,#status code personalisados
    tags=["home"]
    )
def home():
    return{"hello":"world"}


#_________request and response  body_______________________________________
@app.post(
    path="/person/new",
    response_model=personOut,#entra por person y al mandar la respuesta al cliente se manda personOut como respuesta.
    status_code=status.HTTP_201_CREATED,
    tags=["person"],
    summary="create person in the app "
)
def create_person(person: person = Body(...)):# se creea un modelo de la class person y se representa en (def con person )
    """
    create person 

    this path operation a create person in the app and  save the information in the data base

    parameters:
    - request body parameter:
        - **person: person** -> A person model wit first bane, last name, age, hair color and marital status

    Return  a person model with first name, last name , age , hair color and marital status
   
    """
    return person

#_____Validaciones: Query Parameters_______________________________________
@app.get(
    path="/person/detail",
    status_code=status.HTTP_200_OK,
    tags=["person"]
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
    """
    detalles de la persona
    
    este path te envia los detalles de la persona la cual estes buscando  en la base de datos

   - **indaga a la persona**

    """

    return{name:age}

    
#______validaciones path parameters___{person_id}______________________________________
persons = [1,2,3,4,5,6,7,8]

@app.get(
    path="/person/detail/{person_id}",
    status_code=status.HTTP_200_OK,
    tags=["person"]
    )
def show_person(
    person_id: int = Path(
        ...,
        title="person id",
        description="this is the person id . it's  required",
        gt=0,
        example=123
        )
):

    """
    **pass aqui introduce la documentacion (pendiente)**
    """
    if person_id not in persons:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="this person doesn't exists"
        )
   
    return{person_id: "it exists!!"}


# validaciones : request Body

@app.put(
    path="/person/{person_id}",
    status_code=status.HTTP_200_OK,
    tags=["person"]
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
    """
    **pass aqui introduce la documentacion (pendiente)**
    """
    #creando dos request body 
    results = person.dict()#comvertimos el request en dictcionario
    results.update(location.dict())#combinamos person con location con .update
   
    return results#result se le asigna el valor y se retorna 


@app.post(
    path="/login",
    response_model=loginOut,
    status_code=status.HTTP_200_OK,
    tags=["inicio de secion"]
)
def login (username: str=Form(...), password: str = Form(...)):
    """
    ** - pass aqui introduce la documentacion (pendiente)**
    """
    return loginOut(username=username)

#cookies and headers parameters
@app.post(
   path="/conntact",
   status_code=status.HTTP_200_OK,
   tags=["contactos"]
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
    """
    **pass aqui introduce la documentacion (pendiente)**
    """
    return user_agent

#files
@app.post(
    path="/post-image",
    status_code=status.HTTP_200_OK,
    tags=["Uploadfile- imagen"]

    )
def post_image(
    image: UploadFile = File(...)
):
    """
    **pass aqui introduce la documentacion (pendiente)**
    """
    return {
        "filename": image.filename,#optenemos el archivo que queremos subir a la plataforma
        "format": image.content_type,#optenemos el formato del archivo png,jpg entre otros
        "Size(kb)":round(len(image.file.read())/1024,ndigits=2)#round redonde numero  
        #(len)
        #read lee  la capacidad de la imagen 
        #ndigits=agrega dos numeros con punto decimal 
        #operacion:se lee el archivo cuenta los numeros de bytes y los redondea dividido entre 1024
    }

@app.post(
    path="/post-mp4",
    status_code=status.HTTP_200_OK,
    tags=["Uploadfile- video"]
)
def post_mp4(
    video: UploadFile = File(...)

):
    """
    **pass aqui introduce la documentacion (pendiente)**
    """
    return {
        "filename":video.filename,
        "format":video.content_type,
        "Size(kb)":round(len(video.file.read())/1024,ndigits=2)
    }