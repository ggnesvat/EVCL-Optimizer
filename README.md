# EV Charging Location Optimization

This project uses Google's OR-Tools library to solve EV charging location optimization problem. The problem is modeled as a mixed integer programming problem. The objective is to minimize the number of charging stations. The constraints ensure that each vehicle can travel from its origin to its destination without running out of charge.

## Requirements

- Python 3.6 or higher
- OR-Tools Python library

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/ggnesvat/EVCL-Optimizer
   ```
2. Install the requirements:
   ```
   pip install -r requirements.txt
   ```
3. Run the script:
   ```
   python refueling.py
   ```

## Usage

The script reads data from CSV files in the `roads` directory. The `trafik.csv` file contains information about the road network, and the `cities.csv` file contains a list of cities. 

> To obtain the `trafik.csv` file, you can use the `extract.py` script provided in the repository. This script extracts the traffic data from a [PDF report](https://www.kgm.gov.tr/SiteCollectionDocuments/KGMdocuments/Istatistikler/TrafikveUlasimBilgileri/22TrafikUlasimBilgileri.pdf) published by Karayolları Genel Müdürlüğü (General Directorate of Highways) and saves it as a CSV file.

The main script outputs the optimal number of charging stations and their locations.


## License

[MIT](https://choosealicense.com/licenses/mit/)