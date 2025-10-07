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
                raise ValueError("Server information not found for the selected" 
                                 "datapoint.")
            
            if device_info is None:
                raise ValueError("Device information not found for the selected"
                                 "datapoint.")
                
            else: 
                string = self.create_datapoint_annotation_string(x, y,
                                                                 x_label,
                                                                 y_label,
                                                                 device_info,
                                                                 server_info)
                sel.annotation.set(text=string)
                sel.annotation.get_bbox_patch().set(fc="white", alpha=0.8)
                sel.annotation.arrow_patch.set(arrowstyle="simple",
                                               fc="white",
                                               alpha=0.8)                
        plt.grid()
        plt.show()
        
    def get_datapoint_serverinfo(self, 
                                 x_value: float,
                                 y_value: float,
                                 data_types: tuple[str, str]) -> Union[str,
                                                                       None]:
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
            data_types = self.type_checker(data_types)
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
    
    def get_datapoint_upload(self,
                             x_value: float,
                             y_value: float,
                             data_types: tuple[str, str]) -> Union[float,
                                                                   None]:
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
            data_types = self.type_checker(data_types)
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
    
    def get_datapoint_download(self,
                               x_value: float,
                               y_value: float,
                               data_types: tuple[str, str]) -> Union[float,
                                                                     None]:
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
            data_types = self.type_checker(data_types)
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
            data_types = self.type_checker(data_types)
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
    
    def get_datapoint_ping(self,
                           x_value: float,
                           y_value: float,
                           data_types: tuple[str, str]) -> Union[float,
                                                                 None]:
        """Returns the ping for a given datapoint.
        
        Args:
            x_value (float): The x-coordinate value of the datapoint.
            y_value (float): The y-coordinate value of the datapoint.
            data_types (tuple[str, str]): The types of data being plotted.
        Returns:
            Union[float, None]: The ping value if found, else None.
        """
        
        for result in self.data:
            data_types = self.type_checker(data_types)
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
        
        data_type = self.type_checker(data_type)
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
    
    def create_datapoint_annotation_string(self,
                                           x: float,
                                           y: float,
                                           x_label: str,
                                           y_label: str,
                                           device_info: str,
                                           server_info: str ) -> str:
        """Creates a standardized annotation string for datapoints.
        Args: 
            x (float): The x-coordinate value of the datapoint.
            y (float): The y-coordinate value of the datapoint.
            x_label (str): The label for the x-axis.
            y_label (str): The label for the y-axis.
            device_info (str): The device information associated with 
            the datapoint.
            server_info (str): The server information associated with 
            the datapoint.
        Returns:
            str: A formatted annotation string.
        """
        string = ""
        data_type = ()
        
        # Generates a string based on the unused data type
        match self.unused_case:
            case "upload":
                data_type = ("ping", "download")
                data_type = self.type_checker(data_type)
                upload = self.get_datapoint_upload(x, y, data_type)
                string = (f"Server: {server_info}\n"
                         f"{x_label}: {x}\n"
                         f"{y_label}: {y:.2f}\n"
                         f"Upload (mbps): {upload}\n"
                         f"Device: {device_info}")
            case "download":
                data_type = ("ping", "upload")
                data_type = self.type_checker(data_type)
                download = self.get_datapoint_download(x, y, data_type)
                string = (f"Server: {server_info}\n"
                         f"{x_label}: {x}\n"
                         f"{y_label}: {y:.2f}\n"
                         f"Download (mbps): {download}\n"
                         f"Device: {device_info}")
            case "ping":
                data_type = ("download", "upload")
                data_type = self.type_checker(data_type)
                ping = self.get_datapoint_ping(x, y, data_type)
                string = (f"Server: {server_info}\n"
                         f"{x_label}: {x:.2f}\n"
                         f"{y_label}: {y:.2f}\n"
                         f"Ping (ms): {ping}\n"
                         f"Device: {device_info}")
            case _:
                raise ValueError("Invalid unused data type.")
        return string
    
    @staticmethod
    def type_checker(types: tuple[str, str]) -> tuple[str, str]:
        """Ensures that the provided types are valid and in the 
        correct order.
        Args:
            types (tuple[str, str]): A tuple of two data types.
        Returns:
            tuple[str, str]: The validated and ordered tuple of data types.
        """
    
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
    