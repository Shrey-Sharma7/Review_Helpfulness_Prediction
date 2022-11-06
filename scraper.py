import pandas as pd
import requests as requests
from bs4 import BeautifulSoup

# Header File

headers = {
    'authority': 'www.amazon.in',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    # Requests sorts cookies= alphabetically
    # 'cookie': 'session-id=259-7082199-8621237; i18n-prefs=INR; ubid-acbin=257-6335320-8438711; csm-hit=tb:9A9XY8RR7V53WS3H328E+s-9A9XY8RR7V53WS3H328E|1660998351308&t:1660998351308&adb:adblk_no; session-token=g78F2a1rxf+Ixs3gkZUOoHkM4Ld5Q7uwKHApKdbN7/TLuq/ZHYZ+6M+n18ajvf3xn7FKEntK6dTByc93RDNGbUoOZCWGt8w0yxmmsJmfSBVg2YmJIO26me3uB+BTgE/+63o88NPL5JVjIIFMFAJ0N6wxH/AcOecMAx7tjDOFOsfdzrl/WLBxyxFmo7I5iG6QkQXUaJL+FzFBTeCeoZrPg8/sSOtepzx3; session-id-time=2082787201l',
    'device-memory': '8',
    'dnt': '1',
    'downlink': '8.1',
    'dpr': '1.25',
    'ect': '4g',
    'rtt': '100',
    'sec-ch-device-memory': '8',
    'sec-ch-dpr': '1.25',
    'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-ch-viewport-width': '1229',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'service-worker-navigation-preload': 'true',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36',
    'viewport-width': '1229',
}

# Empty Review List

reviewList = []

# Function to get html parsed file for each review page


def get_soup(url):
    r = requests.get(url, headers)
    soup = BeautifulSoup(r.text, "html.parser")
    return soup

# Returns the extracted review in the form of an array which is appended to reviewList


def get_reviews(soup):
    reviews = soup.find_all('div', {'data-hook': 'review'})
    for item in reviews:
        try:
            review = {
                'name': item.find('span', {'class': 'a-profile-name'}).text.strip(),
                'title': item.find('a', {'data-hook': 'review-title'}).text.strip(),
                'rating': item.find('i', {'data-hook': 'review-star-rating'}).text.replace('out of 5 stars', '').strip(),
                # currently in text format
                'date': item.find('span', {'data-hook': 'review-date'}).text.replace('Reviewed in India on', '').strip(),
                'text': item.find('span', {'data-hook': 'review-body'}).text.strip(),
                'helpful_vote': item.find('span', {'data-hook': 'helpful-vote-statement'}).text.strip(),
            }
            reviewList.append(review)
        except:
            pass


for x in range(1, 1000):
    soup = get_soup(
        f'https://www.amazon.in/Milton-Aqua-1000-Stainless-Bottle-Silver/product-reviews/B079R9W1B6/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber={x}')
    print(f'Get Page: {x}')
    get_reviews(soup)

    if not soup.find('li', {'class': 'a-disabled a-last'}):
        pass
    else:
        break

# Convert into CSV

df = pd.DataFrame(reviewList)
csv_file = df.to_csv('waterbottle.csv', index=True)
print('\nCSV String', csv_file)
