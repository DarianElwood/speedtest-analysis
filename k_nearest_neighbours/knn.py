import numpy as np
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import train_test_split
from typing import List, Tuple
from math import radians
from location.location import Location



class KNearestNeighbours:
    def __init__(self, locations: List[Location], n_neighbors: int = 5, use_haversine: bool = True, assume_radians: bool = False, test_size: float = 0.2, random_state: int = 42):
        self.locations = locations
        self.n_neighbors = n_neighbors
        self.use_haversine = use_haversine
        self.assume_radians = assume_radians
        self.test_size = test_size
        self.random_state = random_state
        
        # Store train/test splits for evaluation
        self.X_train = None
        self.X_test = None
        self.y_upload_train = None
        self.y_upload_test = None
        self.y_download_train = None
        self.y_download_test = None
        
        self.model = self._train_model()
    
    def _train_model(self) -> tuple[KNeighborsRegressor, KNeighborsRegressor]:
        coords = np.array([[loc.latitude, loc.longitude] for loc in self.locations])
        uploads = np.array([loc.upload for loc in self.locations])
        downloads = np.array([loc.download for loc in self.locations])

        if self.use_haversine:
            metric = 'haversine'
            if not self.assume_radians:
                coords = np.radians(coords)
        else:
            metric = 'euclidean'

        # Train/test split
        self.X_train, self.X_test, self.y_upload_train, self.y_upload_test, self.y_download_train, self.y_download_test = train_test_split(
            coords, uploads, downloads, 
            test_size=self.test_size, 
            random_state=self.random_state
        )

        # Train separate models for upload and download on training data only
        self.upload_model = KNeighborsRegressor(n_neighbors=self.n_neighbors, metric=metric, weights='distance')
        self.download_model = KNeighborsRegressor(n_neighbors=self.n_neighbors, metric=metric, weights='distance')

        self.upload_model.fit(self.X_train, self.y_upload_train)
        self.download_model.fit(self.X_train, self.y_download_train)

        return (self.upload_model, self.download_model)
    
    def find_nearest(self, lat_rad: float, lon_rad: float) -> List[Tuple[Location, float]]:
        """Find the nearest locations to the given latitude and longitude.
        
        Args:
            lat_rad (float): Latitude in radians.
            lon_rad (float): Longitude in radians.
        """
        
        if self.use_haversine and not self.assume_radians:
            lat_rad = radians(lat_rad)
            lon_rad = radians(lon_rad)

        query_point = np.array([[lat_rad, lon_rad]])
        distances, indices = self.upload_model.kneighbors(query_point)

        nearest_locations = []
        for dist, idx in zip(distances[0], indices[0]):
            nearest_locations.append((self.locations[idx], dist))
        
        return nearest_locations
    
    def evaluate_models(self) -> dict:
        """Evaluate model performance using cross-validation."""
        from sklearn.model_selection import cross_val_score
        from sklearn.metrics import mean_squared_error
        
        coords = np.array([[loc.latitude, loc.longitude] for loc in self.locations])
        uploads = np.array([loc.upload for loc in self.locations])
        downloads = np.array([loc.download for loc in self.locations])
        
        if self.use_haversine and not self.assume_radians:
            coords = np.radians(coords)
        
        # 5-fold cross-validation RMSE
        upload_scores = cross_val_score(self.upload_model, coords, uploads, 
                                       cv=5, scoring='neg_root_mean_squared_error')
        download_scores = cross_val_score(self.download_model, coords, downloads, 
                                         cv=5, scoring='neg_root_mean_squared_error')
        
        return {
            'n_samples': len(self.locations),
            'upload_rmse': -upload_scores.mean(),
            'download_rmse': -download_scores.mean(),
            'upload_rmse_std': upload_scores.std(),
            'download_rmse_std': download_scores.std()
        }

