import math
import unittest
from location.location import Location

class TestLocation(unittest.TestCase):
    def test_haversine_distance_zero(self):
        loc = Location(math.radians(0), math.radians(0), "Origin", 0, 0, 0)
        distance = loc.haversine_distance(math.radians(0), math.radians(0))
        self.assertAlmostEqual(distance, 0.0, places=9)

    def test_haversine_distance_known_points(self):
        # London (51.5074° N, 0.1278° W) to Paris (48.8566° N, 2.3522° E)
        london_lat = math.radians(51.5074)
        london_lon = math.radians(-0.1278)
        paris_lat = math.radians(48.8566)
        paris_lon = math.radians(2.3522)
        loc = Location(london_lat, london_lon, "London", 0, 0, 0)
        distance = loc.haversine_distance(paris_lat, paris_lon)
        # Actual distance ~343 km
        self.assertAlmostEqual(distance, 343, delta=343*0.01)

    def test_haversine_distance_antipodal_points(self):
        # Antipodal points: (0, 0) and (0, pi)
        loc = Location(0, 0, "Origin", 0, 0, 0)
        distance = loc.haversine_distance(0, math.pi)
        expected = math.pi * 6371.0
        self.assertAlmostEqual(distance, expected, delta=expected*1e-6)

    def test_haversine_distance_equator_90_degrees(self):
        # (0, 0) to (0, pi/2) should be quarter circumference
        loc = Location(0, 0, "Equator", 0, 0, 0)
        distance = loc.haversine_distance(0, math.pi/2)
        expected = (math.pi/2) * 6371.0
        self.assertAlmostEqual(distance, expected, delta=expected*1e-6)

if __name__ == "__main__":
    unittest.main()