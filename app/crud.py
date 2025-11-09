from sqlalchemy.orm import Session
from app.models import Address
from app.schemas import AddressCreate, AddressUpdate
from app.utils import haversine

def create_address(db: Session, address: AddressCreate) -> Address:
    """Create and return a new address."""
    db_address = Address(**address.model_dump())
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address

def get_address(db: Session, address_id: int) -> Address | None:
    """Retrieve address by ID."""
    return db.query(Address).filter(Address.id == address_id).first()

def get_addresses(db: Session, skip: int = 0, limit: int = 100) -> list[Address]: 
    """Paginated list of all addresses."""
    return db.query(Address). offset(skip).limit(limit).all()

def update_address(db: Session, address_id: int, address_update: AddressUpdate) -> Address | None:
    """Partial update - only provided fields are changed."""
    db_address = get_address(db, address_id)
    if not db_address:
        return None
    update_data = address_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_address, key, value)
    db.commit()
    db.refresh(db_address)
    return db_address

def delete_address(db: Session, address_id: int) -> bool:
    """Delete address and return success flag."""
    db_address = get_address(db, address_id)
    if not db_address:
        return False
    db.delete(db_address)
    db.commit()
    return True

def get_nearby_addresses(db: Session, latitude: float, longitude: float, max_distance_km: float) -> list[Address]:
    """Return all addresses within max_distance_km using Haversine."""
    all_addresses = db.query(Address).all()
    nearby = []
    for addr in all_addresses:
        dist = haversine(longitude, latitude, addr.longitude, addr.latitude)
        if dist <= max_distance_km:
            nearby.append(addr)
    return nearby
