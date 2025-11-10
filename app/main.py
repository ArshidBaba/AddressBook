import logging
from fastapi import FastAPI, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.database import engine, get_db

# ---------- Logging ----------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)

# ---------- CREATE TABLES SAFELY ----------
try:
    models.Base.metadata.create_all(bind=engine)
    logger.info("Database tables are ready.")
except Exception as e:
    logger.error(f"Could not create tables: {e}")
    raise  # stop the app – you must see the error

# ---------- FastAPI app ----------
app = FastAPI(
    title="Address Book API",
    description="CRUD + geospatial search (SQLite + Haversine)",
    version="1.0.0",
)

@app.get("/", summary="Root endpoint")
def root():
    return {"message": "Welcome  to Address Book API - see /docs for Swagger UI"}

@app.post("/addresses/", 
         response_model=schemas.Address, 
         tags=["addresses"], 
         summary="Create address", 
         description="Create a new address with validated coordinates.",
         )
def create_address(address: schemas.AddressCreate, db: Session = Depends(get_db)):
    logger.info(f"Creating address: {address.label}")
    return crud.create_address(db, address)

@app.get(
    "/addresses/{address_id}",
    response_model=schemas.Address,
    tags=["addresses"],
    summary="Get address by ID",
    )
def read_address(address_id: int, db: Session = Depends(get_db)):
    db_address = crud.get_address(db, address_id)
    if not db_address:
        raise HTTPException(status_code=404, detail="Address not found")
    return db_address

@app.get(
    "/addresses/",
    response_model=list[schemas.Address],
    tags=["addresses"],
    summary="List addresses (paginated)",
)
def read_addresses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_addresses(db, skip=skip, limit=limit)

@app.patch(
    "/addresses/{address_id}",
    response_model=schemas.Address,
    tags=["addresses"],
    summary="Partial update address",
)
def update_address(address_id: int, address_update: schemas.AddressUpdate, db: Session = Depends(get_db)):
    db_address = crud.update_address(db, address_id, address_update)
    if not db_address:
        raise HTTPException(status_code=404, detail="Address not found")
    logger.info(f"Updated address ID {address_id}")
    return db_address

@app.delete(
    "/addresses/{address_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
    tags=["addresses"],
    summary="Delete address",
)
def delete_address(address_id: int, db: Session = Depends(get_db)):
    success = crud.delete_address(db, address_id)
    if not success:
        raise HTTPException(status_code=404, detail="Address not found")
    logger.info(f"Delete address ID {address_id}")
    return None
@app.get(
    "/addresses/nearby/",
    response_model=list[schemas.Address],
    tags=["addresses"],
    summary="Find nearby addresses",
    description="Returns addresses within given distance (km) from coordinates using Haversine formula"
)
def read_nearby_address(
    latitude: float = Query(..., description="Center latitude"),
    longitude: float = Query(..., description="Center longitude"),
    distance_km: float = Query(..., gt=0, description="Max distance in kilometers"),
    db: Session = Depends(get_db),
):
    if not -90 <= latitude <= 90:
        raise HTTPException(status_code=400, detail="Invalid latitude")
    if not -180 <= longitude <= 180:
        raise HTTPException(status_code=400, detail="Invalid longitude")
    
    logger.info(f"Searching nearby within {distance_km}km of ({latitude}, {longitude})")
    return crud.get_nearby_addresses(db, latitude, longitude, distance_km)