"""Module for plotting speed test data using matplotlib and mplcursors 
for interactivity.
"""

import matplotlib.pyplot as plt
import mplcursors
from speedtest_result.speedtest_result import SpeedTestResult
from typing import Union

class DataPlotter:
    """Class to handle plotting of speed test data."""
    
    def __init__(self, data: list[SpeedTestResult]) -> None:
        self.data = data
    
    def plot_data(self, data_types: tuple[str, str]) -> None:
        """Plot the data based on the specified data types.
        Args:
            data_types (tuple[str, str]): A tuple specifying the two 
            data types to plot. Valid options are "ping", "download", 
            and "upload".
            
        Raises:
            ValueError: If the data_types are not valid or if there is 
            no data to plot 
        """
        
        self.unused_case = ""
        x_data, y_data = [], []
        x_label, y_label = "", ""
        
        if not self.data:
            print("No data to plot.")
            return
        
        allowed = {"ping", "download", "upload"}
        if data_types[0] not in allowed or data_types[1] not in allowed:
            raise ValueError(f"Data types must be one of {allowed}")
        
        ## Data extraction based on data types
        match data_types:
            case ("ping", "download"):
                x_data = [result.ping for result in self.data]
                y_data = [result.download for result in self.data]
                x_label, y_label = "Ping (ms)", "Download (Mbps)"
                self.unused_case = "upload"
            case ("ping", "upload"):
                x_data = [result.ping for result in self.data]
                y_data = [result.upload for result in self.data]
                x_label, y_label = "Ping (ms)", "Upload (Mbps)"
                self.unused_case = "download"
            case ("download", "upload"):
                x_data = [result.download for result in self.data]
                y_data = [result.upload for result in self.data]
                x_label, y_label = "Download (Mbps)", "Upload (Mbps)"
                self.unused_case = "ping"
                
            case _:
                raise ValueError("Invalid data type combination.")
        
        ## Plotting
        plt.figure(figsize=(10, 6))
        scatter = plt.scatter(x_data, y_data, c='blue', alpha=0.6, 
                              edgecolors='w', s=100)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(f"Internet Speed Test Results @RRC: {x_label} vs {y_label}")
        
        # Add interactive cursor
        cr = mplcursors.cursor(hover=True)
        cr.add_highlight(scatter)
        # display server info on hover
        @cr.connect("add")
        def on_add(sel):
            x, y = sel.target
            server_info = self.get_datapoint_serverinfo(x, y, data_types)
            device_info = self.get_datapoint_device(x, y, data_types)
            
            if server_info is None:
                sel.annotation.set(text=f"{x_label}: {x:.2f}\n"
                                        f"{y_label}: {y:.2f}")
                
            else: 
                if self.unused_case == "upload":
                    upload = self.get_datapoint_upload(x, y, data_types)
                    sel.annotation.set(text=f"Server: {server_info}\n"
                                            f"{x_label}: {x:.2f}\n"
                                            f"{y_label}: {y:.2f}"
                                            f"\nUpload (mbps): {upload:.2f}"
                                            f"\nDevice: {device_info}")
                elif self.unused_case == "download":
                    download = self.get_datapoint_download(x, y, data_types)
                    sel.annotation.set(text=f"Server: {server_info}\n"
                                            f"{x_label}: {x:.2f}\n"
                                            f"{y_label}: {y:.2f}"
                                            f"\nDownload (mbps): {download:.2f}"
                                            f"\nDevice: {device_info}")
                elif self.unused_case == "ping":
                    ping = self.get_datapoint_ping(x, y, data_types)
                    sel.annotation.set(text=f"Server: {server_info}\n"
                                            f"{x_label}: {x:.2f}\n"
                                            f"{y_label}: {y:.2f}\n"
                                            f"Ping (ms): {ping:.2f}"
                                            f"\nDevice: {device_info}")                   
        plt.grid()
        plt.show()
        
    def get_datapoint_serverinfo(self, x_value: float, y_value: float, data_types: tuple[str, str]) -> Union[str, None]:
        """Returns the server location information for a given
        datapoint.
        If result not found, returns None.
        """
        
        for result in self.data:
            match data_types:
                case ("ping", "download"):
                    if result.ping == x_value and result.download == y_value:
                        return result.server
                case ("ping", "upload"):
                    if result.ping == x_value and result.upload == y_value:
                        return result.server
                case ("download", "upload"):
                    if result.download == x_value and result.upload == y_value:
                        return result.server
        return None
    
    def get_datapoint_upload(self, x_value: float, y_value: float, data_types: tuple[str, str]) -> Union[float, None]:
        """Returns the upload speed for a given datapoint.
        If result not found, returns None.
        """
        
        for result in self.data:
            match data_types:
                case ("ping", "download"):
                    if result.ping == x_value and result.download == y_value:
                        return result.upload
                case ("ping", "upload"):
                    if result.ping == x_value and result.upload == y_value:
                        return result.upload
                case ("download", "upload"):
                    if result.download == x_value and result.upload == y_value:
                        return result.upload
        return None
    
    def get_datapoint_download(self, x_value: float, y_value: float, data_types: tuple[str, str]) -> Union[float, None]:
        """Returns the download speed for a given datapoint.
        If result not found, returns None.
        """
        
        for result in self.data:
            match data_types:
                case ("ping", "download"):
                    if result.ping == x_value and result.download == y_value:
                        return result.download
                case ("ping", "upload"):
                    if result.ping == x_value and result.upload == y_value:
                        return result.download
                case ("download", "upload"):
                    if result.download == x_value and result.upload == y_value:
                        return result.download
        return None

    def get_datapoint_device(self,
                             x_value: float,
                             y_value: float,
                             data_types: tuple[str, str]) -> Union[str, None]:
        """Returns the device for a given datapoint.
        If result not found, returns None.
        """
        
        for result in self.data:
            match data_types:
                case ("ping", "download"):
                    if result.ping == x_value and result.download == y_value:
                        return result.device
                case ("ping", "upload"):
                    if result.ping == x_value and result.upload == y_value:
                        return result.device
                case ("download", "upload"):
                    if result.download == x_value and result.upload == y_value:
                        return result.device
        return None
    
    def get_datapoint_ping(self, x_value: float, y_value: float, data_types: tuple[str, str]) -> Union[float, None]:
        """Returns the ping for a given datapoint.
        """
        
        for result in self.data:
            match data_types:
                case ("ping", "download"):
                    if result.ping == x_value and result.download == y_value:
                        return result.ping
                case ("ping", "upload"):
                    if result.ping == x_value and result.upload == y_value:
                        return result.ping
                case ("download", "upload"):
                    if result.download == x_value and result.upload == y_value:
                        return result.ping
        return None