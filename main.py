import pandas as pd
from dataplotter import DataPlotter
from speedtest_result import SpeedTestResult




def main():
    data = read_data()
    plotter = DataPlotter(data)
    plotter.plot_data(("ping", "download"))
    

def read_data() -> list[SpeedTestResult]:
    data = pd.read_excel('speeds.xlsx')
    data_list = []
    for index, row in data.iterrows():
        result = SpeedTestResult(
            server=row['Server'],
            ping=row['Ping'],
            download=row['Download'],
            upload=row['Upload']
        )
        data_list.append(result)
    return data_list


if __name__ == "__main__":
    main()