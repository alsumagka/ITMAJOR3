from pydantic import BaseModel

class RemindMe(BaseModel):
    type: str
    title: str
    description: str
    day: str

class Movies(BaseModel):
    title: str
    description: str
    day: str

class users(BaseModel):
    username: str
    password: str
    firstname: str
    lastname: str

class ResponseUser(BaseModel):
    username: str
    password: str
    firstname: str
    lastname: str

class ResponseManga(BaseModel):
    type: str
    title: str
    description: str
    day: str

class addManga(BaseModel):
    type: str
    title: str
    description: str
    day: str

class updateManga(BaseModel):
    type: str
    title: str
    description: str
    day: str