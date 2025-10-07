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

## K-NN Regression Analysis Results

The K-NN regression analysis was performed on the speedtest data to evaluate the model's performance in predicting upload and download speeds. The results are summarized below:
- Number of Samples: 108
- Upload Speed RMSE: 18.02 Mbps (Standard Deviation: 10.87 Mbps)
- Download Speed RMSE: 29.69 Mbps (Standard Deviation: 10.55 Mbps)
These results indicate the average error in the model's predictions, with lower RMSE values suggesting better predictive accuracy. The standard deviation provides insight into the variability of the errors across different samples.
This was one of the hardest parts of the project for me, as I had never done any sort of machine learning before. I am gonna sleep for a week now. Bye.

## K-NN Regression Analysis Usage

todo
