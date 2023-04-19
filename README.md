# AirbnbScrapeAndSearcher

*work in progress*



This program runs an Airbnb search and returns what page your listing lands on. Additionally, it scrapes data about your listing and all other listings found in the search, and writes this data to both a .csv and .txt file

To get started, install requirements `bs4` and `scrapy` with pip.

```console
pip3 bs4, scrapy
```

Current Example Usage:

```console
python3 search.py --location=<my-location> --checkin=2023-05-09 --checkout=2023-05-11 --adults=10 --children=0 --infants=0 --pets=0
```

Location must be space-separated with '-' (dashes), and date must be written with `yyyy-mm-dd` formatting.

Children, infants, and pets are optional parameters and will default to 0.
