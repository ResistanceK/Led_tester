from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

app = FastAPI(title = "LED Tester API")

class LED_data(BaseModel):
    voltage: float
    current: float
    color : str
    supply_voltage : float

@app.get("/")
def root():
    return{
	"status" : "ok",
	"message" : "FastAPI LED Tester ready!"
    }

@app.post("/api/measure")
def receive_data(data : LED_data):
    print(f"{datetime.now()}] Received -> {data}")
    return {"status" : "success" , "received" : data}

@app.get("/api/now")
def get_time():
    return {"time" : datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
