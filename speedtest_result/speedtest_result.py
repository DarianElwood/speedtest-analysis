"""Module defining the SpeedTestResult class."""

class SpeedTestResult:
    """Helper class to store individual speed test results."""
    def __init__(self,
                 server: str,
                 ping: float,
                 download: float,
                 upload: float,
                 device: str) -> None:
        self.server = server
        self.ping = ping
        self.download = download
        self.upload = upload
        self.device = device
        
        
    