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
            no data to plot.
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
        data = self.extract_data(data_types)
        x_data, y_data, x_label, y_label, self.unused_case = data
                
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
            """Display additional data when hovering over a point."""
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
        
    def get_datapoint_serverinfo(self, 
                                 x_value: float,
                                 y_value: float,
                                 data_types: tuple[str, str]) -> Union[str, None]:
        """Returns the server location information for a given
        datapoint.
        Args:
            x_value (float): The x-coordinate value of the datapoint.
            y_value (float): The y-coordinate value of the datapoint.
            data_types (tuple[str, str]): The types of data being plotted.
        Returns:
            Union[str, None]: The server information if found, else None.
        """
        
        for result in self.data:
            data_types = type_checker(data_types)
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
                case _:
                    raise ValueError("Invalid data type combination.")
        return None
    
    def get_datapoint_upload(self, x_value: float, y_value: float, data_types: tuple[str, str]) -> Union[float, None]:
        """Returns the upload speed for a given datapoint.
        If result not found, returns None.
        
        Args:
            x_value (float): The x-coordinate value of the datapoint.
            y_value (float): The y-coordinate value of the datapoint.
            data_types (tuple[str, str]): The types of data being plotted.
        
        Returns:
            Union[float, None]: The upload speed if found, else None.
        """
        
        for result in self.data:
            data_types = type_checker(data_types)
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
                case _:
                    raise ValueError("Invalid data type combination.")
        return None
    
    def get_datapoint_download(self, x_value: float, y_value: float, data_types: tuple[str, str]) -> Union[float, None]:
        """Returns the download speed for a given datapoint.
        If result not found, returns None.
        
        Args:
            x_value (float): The x-coordinate value of the datapoint.
            y_value (float): The y-coordinate value of the datapoint.
            data_types (tuple[str, str]): The types of data being plotted.
        Returns:
            Union[float, None]: The download speed if found, else None.
        """
        
        for result in self.data:
            data_types = type_checker(data_types)
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
                case _:
                    raise ValueError("Invalid data type combination.")
        return None

    def get_datapoint_device(self,
                             x_value: float,
                             y_value: float,
                             data_types: tuple[str, str]) -> Union[str, None]:
        """Returns the device for a given datapoint.
        If result not found, returns None.
        
        Args:
            x_value (float): The x-coordinate value of the datapoint.
            y_value (float): The y-coordinate value of the datapoint.
            data_types (tuple[str, str]): The types of data being plotted.
        Returns:
            Union[str, None]: The device if found, else None.
        """
        
        for result in self.data:
            data_types = type_checker(data_types)
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
                case _:
                    raise ValueError("Invalid data type combination.")
        return None
    
    def get_datapoint_ping(self, x_value: float, y_value: float, data_types: tuple[str, str]) -> Union[float, None]:
        """Returns the ping for a given datapoint.
        
        Args:
            x_value (float): The x-coordinate value of the datapoint.
            y_value (float): The y-coordinate value of the datapoint.
            data_types (tuple[str, str]): The types of data being plotted.
        Returns:
            Union[float, None]: The ping value if found, else None.
        """
        
        for result in self.data:
            data_types = type_checker(data_types)
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
                case _:
                    raise ValueError("Invalid data type combination.")
        return None
    
    def extract_data(self, data_type: tuple[str, str]) -> tuple[
                                                    list[float],
                                                    list[float],
                                                    str,
                                                    str,
                                                    str]:
        """Extracts x and y data from the data instance variable, along 
        with labels based on the specified data types.
        
        Args: 
            data_type (tuple[str, str]): A tuple specifying the two 
            data types to extract. Valid options are "ping", "download",
            and "upload".
            
        Returns:
            tuple[list[float], list[float], str, str, str]: A tuple
            containing x data, y data, x label, y label, and the unused
            data type.
            
        Raises:
            ValueError: If the data_types are not valid.
        """
        
        x_data, y_data = [], []
        x_label, y_label = "", ""
        allowed = {"ping", "download", "upload"}
        
        if data_type[0] not in allowed or data_type[1] not in allowed:
            raise ValueError(f"Data types must be one of {allowed}")
    
        # allow either ordering: use the requested order to map x/y
        data_type = type_checker(data_type)
        match data_type:
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
        return (x_data, y_data, x_label, y_label, self.unused_case)
    
def type_checker(types: tuple[str, str]) -> tuple[str, str]:
    """Ensures that the provided types are valid and in the 
    correct order."""
    
    if len(types) != 2:
        raise ValueError("Exactly two data types must be provided.")
    
    if "download" in types and "upload" in types:
        return ("download", "upload")
    elif "ping" in types and "download" in types:
        return ("ping", "download")
    elif "ping" in types and "upload" in types:
        return ("ping", "upload")
    else:
        raise ValueError("Invalid data type combination.")