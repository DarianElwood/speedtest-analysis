# Speedtest Plotter

I created this project out of boredom. We had a class activity at RRC in which everyone had to run a speedtest and enter the results into a shared spreadsheet. I thought it would be fun to visualize the results, so I made this project.

## Features

There is only one main feature of this project: plotting speedtest results. Using the CLI, you can generate a scatter plot of the speedtest results stored in the excel document. You can create plots of any two of the three data types (ping, download speed, upload speed). The third data type will be shown in the annotation for each point.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/darianelwood/speedtestplot.git
    ```
2. Navigate to the project directory:
   ```bash
   cd speedtestplot
   ```
3. Install the required dependencies:
   ```bash
    pip install -r requirements.txt
    ```

## Usage
You can run the script from the command line. Here are some examples:

- Plot download speed vs upload speed, with ping in the annotations:
   ```bash
   python main.py download upload
   ```
- Plot ping vs download speed, with upload speed in the annotations:
   ```bash
    python main.py ping download
    ```
- Plot ping vs upload speed, with download speed in the annotations:
   ```bash
    python main.py ping upload
    ```
