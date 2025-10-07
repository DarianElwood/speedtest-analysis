from location.location import Location
from typing import List
import pandas as pd

class DataProcessor:
    def __init__(self):
        """Initialize the DataProcessor and load data.
         This method loads speed test results and coordinates from
         predefined files and merges them into Location objects.
         The merged data is stored in self.locations as a list of 
         Location instances.
         
            Args:
                None
            Raises:
                None
         """
         
        self.locations: List[Location] = []
        self.load_into_locations()
    
    def load_into_locations(self, excel="speeds.xlsx", csv="coords.csv") -> None:
        """Load and join speed test results with coordinates.
        Raises:
            FileNotFoundError: If the specified files do not exist.
        Returns:
            None
        """
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
        name,lat,long,upload,download.
        Args:
            filepath (str): Path to the CSV file.
        Raises:
            FileNotFoundError: If the specified file does not exist.
            ValueError: If required columns are missing.
        """
        try:
            df = pd.read_csv(filepath)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"File not found: {filepath}") from e
        
        required_columns = {'name', 'lat', 'long', 'upload', 'download'}

        if not required_columns.issubset(df.columns):
                raise ValueError(f"CSV file must contain columns: {required_columns}")
        
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
