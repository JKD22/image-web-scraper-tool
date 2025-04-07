import requests
from bs4 import BeautifulSoup
import os
import argparse
from urllib.parse import urljoin

def fetch_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text

def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup

def extract_image_urls(soup, base_url):
    image_urls = []
    for img_tag in soup.find_all('img'):
        img_url = img_tag.get('src')
        if img_url:
            # Convert relative URL to absolute URL
            img_url = urljoin(base_url, img_url)
            image_urls.append(img_url)
    return image_urls

def save_images(image_urls, folder='images'):
    if not os.path.exists(folder):
        os.makedirs(folder)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0 Safari/537.36'
    }
    for i, img_url in enumerate(image_urls):
        try:
            img_data = requests.get(img_url, headers=headers).content
            with open(os.path.join(folder, f'image_{i+1}.jpg'), 'wb') as img_file:
                img_file.write(img_data)
            print(f"Saved: {img_url}")
        except Exception as e:
            print(f"Failed to save: {img_url} - {e}")

def main(url):
    html = fetch_html(url)
    soup = parse_html(html)
    image_urls = extract_image_urls(soup)
    save_images(image_urls)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scrape images from an Etsy page.')
    parser.add_argument('etsy_url', type=str, help='The URL of the Etsy listing')
    args = parser.parse_args()
    main(args.etsy_url)