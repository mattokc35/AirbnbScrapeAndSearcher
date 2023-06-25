import requests
import sys
import csv
import getopt
from scrapy.selector import Selector
from bs4 import BeautifulSoup

from datetime import date


"""
TODO: export listing name, start external script

"""


"""
Gets all listings
"""


def get_listings(search_page, page_number):
    found = False
    # http get request the url
    answer = requests.get(search_page, timeout=5)
    content = answer.content
    # html parser
    soup = BeautifulSoup(content, 'html.parser')
    # find each listing on page
    listings = soup.find_all('div', 'c4mnd7m')
    for i in range(0, len(listings)):
        # name, subtitle, reviews/ratings
        listing_card_name = listings[i].find(
            'div', {'class': 't1jojoys'}).text
        listing_card_subtitle = listings[i].find(
            'span', {'class': 't6mzqp7'}).text
        listing_card_id = listings[i].find(
            'div', {'class': 't1jojoys dir dir-ltr'}).get('id')[6:]
        if listings[i].find(
                'span', {'class': 't1a9j9y7 r4a59j5 dir dir-ltr'}) == None:
            ratings_reviews = "No Reviews"
        else:
            ratings_reviews = listings[i].find(
                'span', {'class': 't1a9j9y7 r4a59j5 dir dir-ltr'}).get('aria-label')

        # get beds and bedrooms
        beds_bedrooms = listings[i].find_all(
            'span', {'class': ' dir dir-ltr'})
   #     num_beds = beds_bedrooms[0].text
   #     num_bedrooms = beds_bedrooms[1].text
        
        # nightly price
        # if listing is on sale
        if listings[i].find('span', {'class': '_tyxjp1'}) == None:
            current_price = listings[i].find(
                'span', {'class': '_1y74zjx'}).text
            previous_price = listings[i].find(
                'span', {'class': '_1ks8cgb'}).text
        else:
            # else it's not on sale
            current_price = listings[i].find(
                'span', {'class': '_tyxjp1'}).text
            previous_price = "NOT ON SALE"

        current_price = current_price.replace(" ", "")
        # total price
        total_price = listings[i].find_all(
            'span', {'class': 'a8jt5op dir dir-ltr'})[2].text

        # Superhost?
        if listings[i].find(
                'div', {'class': 't1mwk1n0 dir dir-ltr'}) == None:
            super_host = "Not a Superhost or Rare Find"
        else:
            super_host = listings[i].find(
                'div', {'class': 't1mwk1n0 dir dir-ltr'}).text

        # write to txt file
        f.write("NEXT LISTING " + "\n\n\n")
        f.write(listings[i].prettify() + '\n\n\n')
        f.write(listing_card_name + '\n')
        f.write(listing_card_subtitle + '\n\n\n')
        f.write(listing_card_id + '\n')
        f.write("https://airbnb.com/rooms/" + listing_card_id + '\n')
        #f.write(num_beds + '\n')
        #f.write(num_bedrooms + '\n')
        f.write("Current Nightly Price: " + current_price + '\n')
        f.write("Previous Nightly Price: " + previous_price + '\n')
        f.write("Total Price: " + total_price + '\n')
        f.write("Superhost/Rare Find: " + super_host + '\n')
        f.write(ratings_reviews + '\n\n\n')

        # write row to csv file
        #writer.writerow([checkin, checkout, listing_card_name, listing_card_subtitle, num_beds, num_bedrooms,
        writer.writerow([checkin, checkout, listing_card_name, listing_card_subtitle, '=HYPERLINK("https://airbnb.com/rooms/' + listing_card_id + '","URL")', 
                        current_price, previous_price, total_price, super_host, ratings_reviews, location])

        # if my beachhouse is found
        if my_beachhouse in str(listings[i]):
            f.write("FOUND ON PAGE " + str(page_number))
            print("FOUND ON PAGE " + str(page_number))
            found = True
            break
    # Find the next page url
    sel = Selector(text=content)
    next_page = sel.css('a.c1ytbx3a ::attr(href)').extract_first()
    return listings, next_page, found, page_number


"""
Prints the page number that your listing is on, for the specific airbnb search
"""


def listing_found(page_number):

    print("Page Number: " + str(page_number))

    today = date.today()
    historywriter.writerow([today,checkin,checkout,adults,str(page_number),location])
    if (allListings == False):
        sys.exit()


"""
Builds Airbnb search url based on user input parameters
"""


def url_constructor(location, checkin, checkout, adults, children, infants, pets):
    return "https://www.airbnb.com/s/" + location + "/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&date_picker_type=calendar&checkin=" + checkin + "&checkout=" + checkout + "&adults=" + adults + "&children=" + children + "&infants=" + infants + "&pets=" + pets + "&source=structured_search_input_header&search_type=filter_change"


"""
Parses command line arguments (user input)
"""


def command_line_arguments():
    opts, args = getopt.getopt(sys.argv[1:], "hlcoa:kipm",  ["location=", "checkin=", "checkout=",
                                                             "adults=", "children=", "infants=", "pets=", "my_listing="])
    # checking each argument
    for opt, arg in opts:
        if opt == '-h':
            print("Example Arguments:")
            print('--location=<Your-Location> --checkin=2023-01-01 --checkout=2023-01-01 --adults=10 --children=1 --infants=1 --pets=1 --my_listing=<your-listing-id-here>')
            sys.exit()
        elif opt in ("-l", "--location"):
            location = arg
        elif opt in ("-c", "--checkin"):
            checkin = arg
        elif opt in ("-o", "--checkout"):
            checkout = arg
        elif opt in ("-a", "--adults"):
            adults = arg
        elif opt in ("-k", "--children"):
            children = arg
        elif opt in ("-i", "--infants"):
            infants = arg
        elif opt in ("-p", "--pets"):
            pets = arg
        elif opt in ("-m", "--my_listing"):
            my_beachhouse = arg
    return location, checkin, checkout, adults, children, infants, pets, my_beachhouse


# these optional arguments start with a default value
children = "0"
infants = "0"
pets = "0"

# initialize command line arguments
location, checkin, checkout, adults, children, infants, pets, my_beachhouse = command_line_arguments()

# contructs the Airbnb Search URL based on command line arguments
airbnb_url = url_constructor(
    location, checkin, checkout, adults, children, infants, pets)
print(airbnb_url)

# (temporary) put the name of your listing here
listingsTotal = []
pageNumber = 1

print("hi")
# if listings is found
listingFound = False

# if you want all listings
allListings = False

# text file
textFileName = f"data/{checkin}-{checkout}-{location}.txt"
f = open(textFileName, "w", encoding="utf-8")

# history file
historycsvFileName = f"data/history.csv"
historyFile = open(historycsvFileName, 'a', encoding='UTF8')
historywriter = csv.writer(historyFile, lineterminator='\n')

# csv file will be named {checkin-date}-{checkout-date}.csv
csvFileName = f"data/{checkin}-{checkout}-{location}.csv"
csvFile = open(csvFileName, 'w', encoding='UTF8')
writer = csv.writer(csvFile, lineterminator='\n')

# csv header
header = ['Check-in', 'Check-out', 'Listing Card Title', 'Listing Card Subtitle', 'URL', 'Current Nightly Price',
          'Previous Nightly Price', 'Total Price', 'Superhost/Rare Find', 'Ratings/Reviews', 'Location']
writer.writerow(header)

# get listings for first page
listings, next_page_url, found, page_number = get_listings(airbnb_url, 1)
print("hi2")
print(str(found))
if found == True:
    listing_found(page_number)

# print next search url link
print("https://www.airbnb.com" + next_page_url)

# after the first page, we will loop through the rest of the pages
counter = 0
while next_page_url != None and counter <= 14:
    counter += 1
    page_number += 1
    listings, next_page_url, found, page_number = get_listings(
        "https://www.airbnb.com" + next_page_url, page_number)
    print(str(found) + "\n")
    if found == True:
        listing_found(page_number)

    # print next search url link
    if next_page_url != None:
        print("https://www.airbnb.com" + next_page_url)


f.close()
csvFile.close()
