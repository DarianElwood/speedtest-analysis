from location.location import Location
from typing import List
import pandas as pd

class DataProcessor:
    def __init__(self):
        self.locations: List[Location] = []
        self.load_into_locations()
    
    def load_into_locations(self, excel="speeds.xlsx", csv="coords.csv") -> None:
        """Load and join speed test results with coordinates."""
        speeds_df = pd.read_excel(excel)
        coords_df = pd.read_csv(csv)
        
        # Assuming coords.csv has columns: Server, Longitude (radians), Latitude (radians)
        merged_df = pd.merge(speeds_df, coords_df, left_on='Server', right_on='Server')
        location_list = []
        # Create Location objects
        for index, row in merged_df.iterrows():
            loc = Location(
                latitude=row['Latitude (radians)'],
                longitude=row['Longitude (radians)'],
                name=row['Server'],
                download=row['Download'],
                upload=row['Upload']
            )
            self.locations.append(loc)
            
    def load_from_csv(self, filepath: str) -> None:
        """Load locations directly from a CSV file with columns:
        name,lat,long,upload,download
        """
        df = pd.read_csv(filepath)
        for index, row in df.iterrows():
            loc = Location(
                latitude=row['lat'],
                longitude=row['long'],
                name=row['name'],
                upload=row['upload'],
                download=row['download']
            )
            self.locations.append(loc)
            
    def get_locations(self) -> List[Location]:
        return self.locations
