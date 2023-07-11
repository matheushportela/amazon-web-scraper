from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np

# Function to extract Product Title
def get_title(soup):
    try:
        # Outer Tag Object
        title = soup.find("span", attrs={"id": 'productTitle'})
        
        # Inner NavigatableString Object
        title_value = title.text

        # Title as a string value
        title_string = title_value.strip()

    except AttributeError:
        title_string = ""

    return title_string

# Function to extract Product Price
def get_price(soup):
    try:
        # Try finding the price using the class 'a-price-whole'
        price = soup.find("span", attrs={'class': 'a-price-whole'}).string.strip()
    except AttributeError:
        try:
            # If 'a-price-whole' class doesn't exist, try finding the price using 'a-offscreen' class
            price = soup.find("span", attrs={'class': 'a-offscreen'}).string.strip()
        except:
            price = ""
    return price

# Function to extract Product Rating
def get_rating(soup):
    try:
        rating = soup.find("i", attrs={'class': 'a-icon a-icon-star a-star-4-5'}).string.strip()
    except AttributeError:
        try:
            rating = soup.find("span", attrs={'class': 'a-icon-alt'}).string.strip()
        except:
            rating = ""

    return rating

# Function to extract Number of User Reviews
def get_review_count(soup):
    try:
        review_count = soup.find("span", attrs={'id': 'acrCustomerReviewText'}).string.strip()
    except AttributeError:
        review_count = ""

    return review_count

# Function to extract Availability Status
def get_availability(soup):
    try:
        available = soup.find("div", attrs={'id': 'availability'})
        available = available.find("span").string.strip()
    except AttributeError:
        available = "Not Available"

    return available

if __name__ == '__main__':
    # add your user agent (https://httpbin.org/get)
    HEADERS = ({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 OPR/98.0.0.0',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7'
    })

    var = 'playstation 5'
    # The webpage URL
    URL = "https://www.amazon.com.br/s?k=" + var.replace(' ', '+')

    # HTTP Request
    webpage = requests.get(URL, headers=HEADERS)

    # Soup Object containing all data
    soup = BeautifulSoup(webpage.content, "html.parser")

    # Fetch links as List of Tag Objects
    links = soup.find_all("a", attrs={'class': 'a-link-normal s-no-outline'})

    # Store the links
    links_list = []

    # Loop for extracting links from Tag Objects
    for link in links:
        links_list.append(link.get('href'))

    # Initialize empty lists for each column
    titles = []
    prices = []
    ratings = []
    reviews = []
    availabilities = []

    # Loop for extracting product details from each link
    for link in links_list:
        new_webpage = requests.get("https://www.amazon.com.br" + link, headers=HEADERS)
        new_soup = BeautifulSoup(new_webpage.content, "html.parser")

        # Append values to respective lists
        titles.append(get_title(new_soup))
        prices.append(get_price(new_soup))
        ratings.append(get_rating(new_soup))
        reviews.append(get_review_count(new_soup))
        availabilities.append(get_availability(new_soup))
        print(get_title(new_soup) + '|' + get_price(new_soup) + '|' + get_rating(new_soup) + '|' +
              get_review_count(new_soup) + '|' + get_availability(new_soup))

    # Create a dictionary with the lists
    data = {
        "title": titles,
        "price": prices,
        "rating": ratings,
        "reviews": reviews,
        "availability": availabilities
    }

    amazon_df = pd.DataFrame(data)
    amazon_df['title'].replace('', np.nan, inplace=True)
    amazon_df = amazon_df.dropna(subset=['title'])
    amazon_df.to_csv("amazon_data.csv", header=True, index=False)
