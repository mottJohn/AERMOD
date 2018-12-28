# About the Project
Aermod is used to modle construction phase dust emission, including TSP, RSP, and FSP. To run the model, several input files are needed, and preparation of those files is time consuming without smarter tools. 

The project aims at developing scripts that can speed up the data preparation process.

# Get Started

1. Download the scripts to your local directory
2. hourlyEmissionRate.py is used to prepare hourly emission factor for model input
    * noted that EF is project specific. You need to change the scripts a bit to cater your need
    * what you can leverage is the format generated through the code which has been proved working
3. mcipPreparation.py is used to prepare meteorological data for model input
    * This is Hong Kong specific. The requirements are set by EPD HK
4. resultSummary.py is used to prepare summary tables for presentation in report
    * The summary parameters are based on Hong Kong Air Quality Objectives
    * It is therefore also Hong Kong specific