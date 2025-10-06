"""Module for plotting speed test data using matplotlib and mplcursors 
for interactivity.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
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
        
        if not self.data:
            print("No data to plot.")
            return
        
        allowed = {"ping", "download", "upload"}
        if data_types[0] not in allowed or data_types[1] not in allowed:
            raise ValueError(f"Data types must be one of {allowed}")
        
        match data_types:
            case ("ping", "download"):
                x_data = [result.ping for result in self.data]
                y_data = [result.download for result in self.data]
                x_label, y_label = "Ping (ms)", "Download (Mbps)"
            case ("ping", "upload"):
                x_data = [result.ping for result in self.data]
                y_data = [result.upload for result in self.data]
                x_label, y_label = "Ping (ms)", "Upload (Mbps)"
            case ("download", "upload"):
                x_data = [result.download for result in self.data]
                y_data = [result.upload for result in self.data]
                x_label, y_label = "Download (Mbps)", "Upload (Mbps)"
            case _:
                raise ValueError("Invalid data type combination.")
        
        ## Plotting
        plt.figure(figsize=(10, 6))
        scatter = plt.scatter(x_data, y_data, c='blue', alpha=0.6, 
                              edgecolors='w', s=100)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(f"Scatter plot of {x_label} vs {y_label}")
        
        # Add interactive cursor
        cr = mplcursors.cursor(hover=True)
        cr.add_highlight(scatter)
        @cr.connect("add")
        def on_add(sel):
            x, y = sel.target
            server_info = self.get_datapoint_serverinfo(x, y, data_types)
            if server_info:
                sel.annotation.set(text=f"Server: {server_info}\n"
                                        f"{x_label}: {x:.2f}\n"
                                        f"{y_label}: {y:.2f}")
            else:
                sel.annotation.set(text=f"{x_label}: {x:.2f}\n"
                                        f"{y_label}: {y:.2f}")
        plt.grid()
        plt.show()
        
    def get_datapoint_serverinfo(self, x_value: float, y_value: float, data_types: tuple[str, str]) -> Union[str, None]:
        """Returns the server location information for a given
        datapoint.
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
    
