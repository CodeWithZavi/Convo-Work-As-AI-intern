

from fastapi import FastAPI  #frame work import FastAPI
from pydantic import BaseModel # help in validation like data send and recive for checking validation
#override on base model  ( one for send and one for recive)
from typing import List

app = FastAPI()  # create app object

class Tea(BaseModel):
    id: int
    name: str
    orgin: str  


teas:List[Tea] = []

# all this is data structure define here

#decorator define get method
@app.get("/")  # decorator define get method
def read_root():
    return {"message": "Welcome to the Tea API"}  # return welcome message


#function 
@app.get("/teas")
def get_teas():
    return teas  # return list of teas

@app.post("/teas")

def add_tea(tea: Tea):  # cuz  of pydantic we can use Tea model here
    teas.append(tea)  
    return tea  # return the added tea

@app.put("/teas/{tea_id}")
def update_tea(tea_id: int, updated_tea: Tea):

 for index, tea in enumerate(teas):
    if tea.id == tea_id:
        teas[index] = updated_tea
        return updated_tea

    return {"error": "Tea not found"}  # if tea not found
 
@app.delete("/teas/{tea_id}")
def delete_tea(tea_id: int):
    for index, tea in enumerate(teas):
        if tea.id == tea_id:
            deleted_tea = teas.pop(index)
            return deleted_tea

    return {"error": "Tea not found"}  # if tea not found

