import math
from abc import ABC, abstractmethod

class Location():
    def __init__(self, latitude: float, longitude: float, name: str,
                 upload: float, download: float, ping: float):
        """Location class constructor.
        Args:
            latitude (float): Latitude in radians.
            longitude (float): Longitude in radians.
            name (str): Name of the location.
            
        Raises:
            TypeError: If latitude or longitude are not numeric types.
            ValueError: If latitude or longitude are out of valid range.
        """
        
        self.latitude = latitude
        self.longitude = longitude
        self.upload = upload
        self.download = download
        self.ping = ping
        
        if not isinstance(ping, (int, float)):
            raise TypeError("Ping must be a numeric type.")
        
        if not isinstance(download, (int, float)):
            raise TypeError("Download speed must be a numeric type.")
        
        if not isinstance(upload, (int, float)):
            raise TypeError("Upload speed must be a numeric type.")
        
        if not isinstance(latitude, (int, float)):
            raise TypeError("Latitude must be a numeric type.")
        
        if not isinstance(longitude, (int, float)):
            raise TypeError("Longitude must be a numeric type.")
        
        if not self.is_valid_coordinate(latitude, longitude):
            raise ValueError("Invalid latitude or longitude values.")
        
        self.name = name

    @staticmethod
    def is_valid_coordinate(lat_rad, lon_rad):
        return (
            -math.pi/2 <= lat_rad <= math.pi/2 and
            -math.pi <= lon_rad <= math.pi
        )

    def haversine_distance(self, lat_rad: float, lon_rad: float) -> float:
        """Calculate the Haversine distance between this location and another point.
        
        Args:
            lat_rad (float): Latitude of the other point in radians.
            lon_rad (float): Longitude of the other point in radians.
        """
        
        R = 6371.0  # Earth radius in kilometers
        dlat = lat_rad - self.latitude
        dlon = lon_rad - self.longitude

        a = (math.sin(dlat / 2) ** 2 +
             math.cos(self.latitude) * math.cos(lat_rad) * math.sin(dlon / 2) ** 2)
        c = 2 * math.asin(math.sqrt(a))
        distance = R * c
        return distance