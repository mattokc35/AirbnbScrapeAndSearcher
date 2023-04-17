import requests
from scrapy.selector import Selector
import sys

from bs4 import BeautifulSoup


"""
TODO: write data to .csv/excel file, implement command line inputs

"""

# (temporary) input your Airbnb search url here
airbnb_url = ""
# (temporary) put the name of your listing here
my_beachhouse = ""

listingsTotal = []
pageNumber = 1

# if listings is found
listingFound = False

# if you want all listings
allListings = False

# file
f = open("dataFile.txt", "a", encoding="utf-8")



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

        if listings[i].find(
                'span', {'class': 't5eq1io r4a59j5 dir dir-ltr'}) == None:
            ratings_reviews = "No Reviews"
        else:
            ratings_reviews = listings[i].find(
                'span', {'class': 't5eq1io r4a59j5 dir dir-ltr'}).get('aria-label')

        # get beds and bedrooms
        beds_bedrooms = listings[i].find_all(
            'span', {'class': 'dir dir-ltr'})
        num_beds = beds_bedrooms[0].text
        num_bedrooms = beds_bedrooms[1].text

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
        print(ratings_reviews)
        print(super_host)

        # write to file
        f.write("NEXT LISTING " + "\n\n\n")
        #f.write(listings[i].prettify() + '\n\n\n')
        f.write(listing_card_name + '\n')
        f.write(listing_card_subtitle + '\n')
        f.write(num_beds + '\n')
        f.write(num_bedrooms + '\n')
        f.write("Current Nightly Price: " + current_price + '\n')
        f.write("Previous Nightly Price: " + previous_price + '\n')
        f.write("Total Price: " + total_price + '\n')
        f.write("Superhost/Rare Find: " + super_host + '\n')
        f.write(ratings_reviews + '\n\n\n')

        # my beachhouse is founds
        if my_beachhouse in listings[i].get_text():
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
    if (allListings == False):
        sys.exit()


listings, next_page_url, found, page_number = get_listings(airbnb_url, 1)

print(str(found))
if found == True:
    listing_found(page_number)


# after the first page we will go through each page and add listings to listingsTotal
counter = 0
while next_page_url != None and counter <= 14:
    counter += 1
    page_number += 1
    listings, next_page_url, found, page_number = get_listings(
        "https://www.airbnb.com" + next_page_url, page_number)
    print(str(found))
    if found == True:
        listing_found(page_number)


f.close()
