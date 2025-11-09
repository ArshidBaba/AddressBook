from math import radians, sin, cos, sqrt, asin


def haversine(lon1: float, lat1: float, lon2: float, lat2: float) -> float:
    """
    Calculate great-circle distance between two points on Earth (in kilometers).
    Uses Haversine formula - accurate for all distances.
    """
    # Convert to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # Earth's radius in kilometers
    return c * r