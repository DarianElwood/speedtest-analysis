import pandas as pd
from dataplotter import DataPlotter
from speedtest_result import SpeedTestResult
import sys

def main() -> None:
    """Main function to read data and plot based upon command-line 
    arguments."""
    
    data = read_data()
    plotter = DataPlotter(data)
    match sys.argv:
        case [_, x_type, y_type] if x_type in {"ping", "download", "upload"} and y_type in {"ping", "download", "upload"}:
            plotter.plot_data((x_type, y_type))
        case _:
            print("Usage: python main.py <x_data_type> <y_data_type>")
            print("Data types must be one of 'ping', 'download', or 'upload'.")
            sys.exit(1)
    

def read_data() -> list[SpeedTestResult]:
    """Reads speed test data from an Excel file and returns a list of 
    SpeedTestResult objects.
    
    Returns:
        list[SpeedTestResult]: List of speed test results.
    """
    
    data = pd.read_excel('speeds.xlsx')
    data_list = []
    for index, row in data.iterrows():
        result = SpeedTestResult(
            server=row['Server'],
            ping=row['Ping'],
            download=row['Download'],
            upload=row['Upload'],
            device=row['Device'],
        )
        data_list.append(result)
    return data_list


if __name__ == "__main__":
    main()