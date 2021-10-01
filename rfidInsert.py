import sys

sys.dont_write_bytecode = True

########################################

import requests
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_utils.tasks import repeat_every

import rfidReader

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

class d:
    def __init__( self ):
        self.oTagID = '0'
        self.cProduct = None

url = 'dodo dodo dodo do'
data = d()

@app.on_event('startup')
async def startup_event():
    global rfid
    rfid = rfidReader.rfid()
    rfid.rfidOpen()
    await rfidReadNInsert()
    
@app.on_event('shutdown')
def shutdown_event():
    rfid.rfidClose()

@repeat_every( seconds = 30, wait_first = True )
def rfidReadNInsert() -> None:
    nTagID = rfid.getTagID()
    if( nTagID == '0' ):
        return
    if( data.oTagID != nTagID and data.cProduct != None ):
        r = requests.post( url+'/insert', json = { 'tagID': nTagID, 'lotID': data.cProduct } )
        data.oTagID = nTagID
        data.cProduct = None

@app.get('/test')
def test():
    return rfid.getVersion()

@app.get('/sendProductID')
def recieveProductID( lotID: str ):
    data.cProduct = lotID

@app.get('/lotID')
def getLotID():
    return data.cProduct

if __name__ == "__main__":
    uvicorn.run( app, host = '0.0.0.0' )
