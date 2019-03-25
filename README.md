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
    * Beware of the units. Sometimes, the model update will change the input units.
4. parsePOS.py is used to parse the .POS file from AERMOD output.
    * Put all POS files in one folder. The program will extract all for you.
    * The program output excels in a certain format. The reason to use this strange format is for compatability of another Excel Macro which intends to do the same thing.
5. resultSummary.py is used to prepare summary tables for presentation in report
    * Put each kind of polluntants in separate folders, e.g. TSPhr, FSPda, etc. Don't put them all together.
    * The summary parameters are based on Hong Kong Air Quality Objectives
    * It is therefore also Hong Kong specific
    
# Quickier Way to Do Box
ST_subdivide
ST_extent

# Quickier Way to Do Scaling
Get the vertex of polygons. Find the closer points to a particilar point. Scale the rectangles using the closer point as anchor.
ST_dumppoints, ST_scale
