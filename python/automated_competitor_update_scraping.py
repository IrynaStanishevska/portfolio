import requests
from lxml import html
import hashlib
import re
import os
from datetime import datetime

# URL to scrape
URL = "https://www.XXXX.co.uk/annual-travel-insurance/"

# Directory to save content and hash
CONTENT_DIR = "content_changes"
HASH_FILE = "last_content_hash.txt"

# Create directory to save content if it doesn't exist
os.makedirs(CONTENT_DIR, exist_ok=True)

# Function to fetch page content
def fetch_page_content(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text

# Function to extract relevant content using XPath
def extract_relevant_content(page_content):
    tree = html.fromstring(page_content)

    # Select the required sections using XPath
    sections = []

    try:
        sections.append(tree.xpath('//div[@class="newyear-commercial-banner"]')[0])
    except IndexError:
        pass

    try:
        sections.append(tree.xpath(
            '//section[@class="hero-section st-product-bg single-trip-banner content-media-banner half-img-banner"]')[0])
    except IndexError:
        pass

    try:
        sections.append(tree.xpath('//section[@id="do-i-need-travel-insurance"]')[0])
    except IndexError:
        pass

    try:
        sections.append(tree.xpath(
            '//section[contains(@class, "manage-your-policy-section") and contains(., "What’s not covered?")]')[0])
    except IndexError:
        pass

    try:
        sections.append(tree.xpath(
            '//section[contains(@class, "manage-your-policy-section") and contains(., "How much does annual travel insurance cost?")]')[0])
    except IndexError:
        pass

    # Convert the selected sections to text and concatenate them
    content = ""
    for section in sections:
        content += html.tostring(section, pretty_print=True, encoding='unicode')

    # Remove CSS and @media blocks using regular expressions
    content = re.sub(r'<style.*?>.*?</style>', '', content, flags=re.DOTALL)
    content = re.sub(r'<script.*?>.*?</script>', '', content, flags=re.DOTALL)
    content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
    content = re.sub(r'\s*\{[^}]*\}', '', content, flags=re.DOTALL)

    # Remove all HTML tags, leaving only text, while preserving formatting
    content = re.sub(r'<[^>]+>', '', content)
    content = re.sub(r'\n\s*\n', '\n', content)  # Remove extra blank lines
    content = content.strip()  # Remove leading and trailing whitespace

    return content

# Function to compute hash of the content
def compute_hash(content):
    return hashlib.sha256(content.encode('utf-8')).hexdigest()

# Function to read the last content hash from file
def read_last_content_hash():
    if os.path.exists(HASH_FILE):
        with open(HASH_FILE, 'r') as file:
            return file.read().strip()
    return None

# Function to save the current content hash to file
def save_current_content_hash(content_hash):
    with open(HASH_FILE, 'w') as file:
        file.write(content_hash)

# Function to save content to file
def save_content(content):
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    content_filename = os.path.join(CONTENT_DIR, f"{timestamp}.txt")
    with open(content_filename, 'w') as content_file:
        content_file.write(content)
    print(f"Content saved to: {content_filename}")

# Main script
def main():
    page_content = fetch_page_content(URL)
    content = extract_relevant_content(page_content)
    current_content_hash = compute_hash(content)

    last_content_hash = read_last_content_hash()

    if current_content_hash != last_content_hash:
        print("Content has changed!")
        save_content(content)
        save_current_content_hash(current_content_hash)
    else:
        print("Content has not changed.")

if __name__ == "__main__":
    main()
