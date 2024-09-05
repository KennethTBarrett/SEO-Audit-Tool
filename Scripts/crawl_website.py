import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def is_internal_link(base_url, link):
    """Check whether link is internal before navigating"""
    return urlparse(link).netloc == "" or urlparse(link).netloc == urlparse(base_url).netloc


def crawl_website(url, visited=None):
    """Crawls internal links"""
    if visited is None:
        visited = set()

    # Normalize URL
    url = url if url.endswith('/') else url + '/'

    if url in visited:
        return
    
    visited.add(url)

    try:
        # Fetch page content
        response = requests.get(url)
        if response.status_code != 200:
            return f"Failed to retrieve {url}, status code: {response.status_code}"
        
        soup = BeautifulSoup(response.text, 'html.parser')

        for link in soup.find_all('a', href=True):
            href = link['href']
            
            next_page = urljoin(url, href)

            if is_internal_link(url, next_page):
                if next_page not in visited:
                    crawl_website(next_page, visited)

    except requests.RequestException as e:
        return f"Error crawling {url}, status code: {e}"
    
