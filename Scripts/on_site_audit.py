"""This file exists to evaluate the presence and length of
    title tags, meta descriptions, and H1 Headers"""


import requests
from bs4 import BeautifulSoup


def fetch(url):
    """Fetches URL input and returns text for further use.
        Raises exception if there was an error."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as ex:
        print(f"There was an issue fetching {url}: {ex}")
        return None


def check_ssl_enabled(url):
    """Checks whether the website has SSL enabled."""
    return url.startswith('https://')


def parse(html):
    """Parses html"""
    soup = BeautifulSoup(html, 'lxml')
    return soup


def check_title_len(soup):
    """Checks title length."""
    title = soup.title.strong if soup.title else None
    if title and 51 <= len(title) <= 60:
        return f"Title tag is present: '{title}' and of acceptable length {len(title)}"
    elif title and len(title) > 60:
        return f"Title tag is present: '{title}', but is too long ({len(title)} characters). Try to keep it under 60 characters to avoid truncation."
    elif title and len(title) < 51:
        return f"Title tag is present: '{title}', and you have room to include up to {60-len(title)} more characters."
    else:
        return "Title tag is missing! Include a title with 51-60 characters."


def check_meta_descr_len(soup):
    """Checks meta description length."""
    meta_descr = soup.find('meta', attrs={'name': 'description'})
    if meta_descr and meta_descr.get('content'):
        descr = meta_descr['content']
        if 150 <= len(descr) <= 160:
            return "Meta description is present and of optimal length."
        elif len(descr) > 160:
            return f"Meta description is present but too long ({len(descr)} characters). Keep the description under 160 characters to avoid truncation."
        elif len(descr) < 150:
            return f"Meta description is present, and you have room to include up to {160-len(meta_descr)} more charcters."
    else:
        return "Meta description is missing! Include a meta description with 150-160 characters."



def check_num_h1(soup):
    """Checks whether H1 tag exists, or if there are multiple."""
    h1_tags = soup.find_all('h1')
    if len(h1_tags) == 1:
        return "There is one H1 tag on this page, which is optimal."
    elif len(h1_tags) > 1:
        return "There are multiple H1 tags on this page. Ensure you only have one unique H1 tag per page."
    else:
        return "There is no H1 tag on this page. Be sure to include one!"
