import requests
from bs4 import BeautifulSoup
import re
import json
from datetime import datetime

# Headers to mimic a browser visit
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
}

# Function to check backlinks and noindex tag
def check_backlinks_and_noindex(domain):
    with open('/Users/irina/Web-Scraping-Tasks/guest_posting/backlinks.txt', 'r') as f:
        urls = f.readlines()

    output = []

    for url in urls:
        url = url.strip()
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Check if the noindex tag is present
            noindex_present = soup.find('meta', {'name': 'robots', 'content': 'noindex'}) is not None
            if noindex_present:
                print(f"'noindex' tag found on {url}")
                output.append({
                    'url': url,
                    'noindex': True
                })

            # Check for backlinks
            backlink_found = re.search(domain, response.text)
            if backlink_found:
                print(f"Backlink to {domain} found on {url}")
                output.append({
                    'url': url,
                    'backlink_found': True
                })
            else:
                output.append({
                    'url': url,
                    'backlink_found': False
                })
        else:
            print(f"Failed to access {url}, status code: {response.status_code}")
            output.append({
                'url': url,
                'error': f"Failed to access, status code: {response.status_code}"
            })

    # Save the output to a JSON file
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    output_file = f"backlinks_output_{timestamp}.json"
    with open(output_file, 'w') as outfile:
        json.dump(output, outfile, indent=4)

    print(f"Results saved to {output_file}")

# Example usage
domain = "https://www.globelink.co.uk/"
check_backlinks_and_noindex(domain)
