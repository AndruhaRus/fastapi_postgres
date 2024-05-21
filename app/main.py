# app/main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import requests
import os

DATABASE_URL = "postgresql+psycopg2://user:password@db:5432/fastapi_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app = FastAPI()

class Address(Base):
    __tablename__ = "addresses"
    address = Column(String, primary_key=True, index=True)
    latitude = Column(String, index=True)
    longitude = Column(String, index=True)

Base.metadata.create_all(bind=engine)

class AddressRequest(BaseModel):
    address: str

@app.post("/get_coordinates/")
async def get_coordinates(address_request: AddressRequest):
    db = SessionLocal()
    address = address_request.address
    
    db_address = db.query(Address).filter(Address.address == address).first()
    if db_address:
        db.close()
        return {"address": db_address.address, "latitude": db_address.latitude, "longitude": db_address.longitude}
    
    geocode_api_url = "https://geocode.xyz"
    response = requests.get(f"{geocode_api_url}/{address}?json=1")
    data = response.json()
    
    if "error" in data:
        db.close()
        raise HTTPException(status_code=400, detail="Geocoding API error")

    latitude = data.get("latt")
    longitude = data.get("longt")

    new_address = Address(address=address, latitude=latitude, longitude=longitude)
    db.add(new_address)
    db.commit()
    db.refresh(new_address)
    db.close()

    return {"address": new_address.address, "latitude": new_address.latitude, "longitude": new_address.longitude}
