"""Module defining the SpeedTestResult class."""

class SpeedTestResult:
    """Helper class to store individual speed test results.
    Args: 
        server (str): The server used for the speed test.
        ping (float): The ping result in milliseconds.
        download (float): The download speed in Mbps.
        upload (float): The upload speed in Mbps.
        device (str): The device on which the test was conducted.
    Attributes:
        server (str): The server used for the speed test.
        ping (float): The ping result in milliseconds.
        download (float): The download speed in Mbps.
        upload (float): The upload speed in Mbps.
        device (str): The device on which the test was conducted.
    Methods:
        __init__: Initializes a SpeedTestResult instance with the 
        provided parameters.
        
    """
    
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
        
        
    