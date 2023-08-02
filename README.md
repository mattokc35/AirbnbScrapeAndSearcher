*work in progress*



This program runs an Airbnb search and returns what page your listing lands on. Additionally, it scrapes data about your listing and all other listings found in the search, and writes this data to both a .csv and .txt file
# AirbnbScrapeAndSearcher


This program runs an Airbnb searches and returns what page your listing lands on for each search. Additionally, it scrapes data about your listing and all other listings found in the search, and writes this data to both a .csv and .txt file.

# Installing Requirements

To get started, install requirements `bs4` and `scrapy` with pip.

```console
pip3 bs4, scrapy
```

# Running the Program

Put your search parameters in the `InputParameters.csv` file. 

Location must be space-separated with '-' (dashes), and date must be written with `yyyy-mm-dd` formatting.

Children, infants, and pets are optional parameters and will default to 0.

Each line in the CSV file will correspond to new Airbnb search that will be performed by `search.py`.

To run the program, simply run

```console
python3 script.py
```


Alternatively, you can run search.py individually and input your parameters manually as such: 

```console
python3 search.py --location=<my-location> --checkin=2023-05-09 --checkout=2023-05-11 --adults=10 --children=0 
                  --infants=0 --pets=0 --my_listing=<your-listing-id-here>
```


