import requests
from bs4 import BeautifulSoup
import os

def fetch_html(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup

def extract_image_urls(soup):
    image_urls = []
    for img_tag in soup.find_all('img'):
        img_url = img_tag.get('src')
        if img_url:
            image_urls.append(img_url)
    return image_urls

def save_images(image_urls, folder='images'):
    if not os.path.exists(folder):
        os.makedirs(folder)
    for i, img_url in enumerate(image_urls):
        img_data = requests.get(img_url).content
        with open(os.path.join(folder, f'image_{i+1}.jpg'), 'wb') as img_file:
            img_file.write(img_data)

def main(url):
    html = fetch_html(url)
    soup = parse_html(html)
    image_urls = extract_image_urls(soup)
    save_images(image_urls)

if __name__ == "__main__":
    etsy_url = 'https://www.etsy.com/listing/your-specific-listing'
    main(etsy_url)