class SpeedTestResult:
    def __init__(self, server: str, ping: float, download: float, upload: float) -> None:
        self.server = server
        self.ping = ping
        self.download = download
        self.upload = upload
        
    