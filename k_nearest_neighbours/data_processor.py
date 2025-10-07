from location.location import Location
import pandas as pd

class DataProcessor:
    def __init__(self):
        self.data = []
    
    def load_data(self):
        """Load data from an Excel file and store it in self.data."""
        df = pd.read_excel("speeds.xlsx")
        df2 = pd.read_csv('coords.csv')
        results = []
        for index, row in df.iterrows():
            coords = df2[df2['Server'] == row["Server"]][['Latitude (radians)', 'Longitude (radians)']].values
            if coords.size == 0:
                continue
            lat, lon = coords[0]
            print(lat, lon)
            results.append([row["Server"], row["Upload"], row["Download"], row["Ping"], lat, lon])
            