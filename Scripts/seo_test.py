import subprocess
import tempfile
import os
import requests
import shutil
import json
from bs4 import BeautifulSoup

def fetch(url):
    '''Fetches URL input and returns text for further use. Raises exception if there was an error.'''
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as ex:
        print(f"There was an issue fetching {url}: {ex}")
        return None

def check_ssl_enabled(url):
    '''Checks whether the website has SSL enabled.'''
    return url.startswith('https://')    

def parse(html):
    '''Parses html'''
    soup = BeautifulSoup(html, 'lxml')
    return soup

def check_title_len(soup):
    '''Checks title length'''
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
    '''Checks meta description length.'''
    meta_descr = soup.find('meta', attrs={'name': 'description'})
    if meta_descr and meta_descr.get('content'):
        descr = meta_descr['content']
        if 150 <= len(descr) <= 160:
            return "Meta description is present and of optimal length."
        elif len(descr) > 160:
            return f"Meta description is present but too long ({len(descr)} characters). Keep the description under 160 characters to avoid truncation."
        elif len(descr) < 150:
            return f"Meta description is present, and you have room to include up to {160-len(title)} more charcters."
    else:
        return "Meta description is missing! Include a meta description with 150-160 characters."
        
def check_num_h1(soup):
    '''Checks whether H1 tag exists, or if there are multiple.'''
    h1_tags = soup.find_all('h1')
    if len(h1_tags) == 1:
        return "There is one H1 tag on this page, which is optimal."
    elif len(h1_tags) > 1:
        return "There are multiple H1 tags on this page. Ensure you only have one unique H1 tag per page."
    else:
        return "There is no H1 tag on this page. Be sure to include one!"

def check_lighthouse_installed():
    """Check if Lighthouse is installed and accessible."""
    if not shutil.which('lighthouse'):
        raise EnvironmentError("Lighthouse is not installed or not found in PATH. Please install it using 'npm install -g lighthouse'.")
    
def run_lighthouse(url, output_path):
    try:
        # Run Lighthouse using subprocess and output results to a JSON object.
        lighthouse_path = r'C:\Users\kenne\Downloads\seo_checker_venv\Scripts\lighthouse.cmd'
        subprocess.run([
            lighthouse_path, url,
            '--output=json',
            '--output-path', output_path,
            '--chrome-flags="--headless"'
        ], check=True)

        # Return the Lighthouse report
        with open(output_path, 'r', encoding='utf-8') as file:
            report = json.load(file)
        return report
    
    except subprocess.CalledProcessError as e:
        print(f"Error running Lighthouse: {e}")
        return None
    
def read_performance_metrics(report):
    if report:
        # Extract metrics from report produced by Lighthouse
        performance_score = report['categories']['performance']['score']
        first_contentful_paint = report['audits']['first-contentful-paint']['displayValue']
        speed_idx = report['audits']['speed-index']['displayValue']
        time_to_interactive = report['audits']['interactive']['displayValue']

        return {
            'Performance Score': performance_score * 100,
            'First Contentful Paint': first_contentful_paint,
            'Speed Index': speed_idx,
            'Time to Interactive': time_to_interactive
        }
    return None

def main():
    '''Currently only checks lighthouse; to be updated'''
    url = input("Please enter the URL: ")
    if url.__contains__('http'):
        pass
    else:
        url = f'http://{url}'
    
    with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as temp_file:
        output_path = temp_file.name

    report = run_lighthouse(url, output_path)
    metrics = read_performance_metrics(report)

    if metrics:
        print(f"Performance Metrics for {url}:")
        for m, v in metrics.items():
            print(f"{m}: {v}")

    # Cleaning up the temp file
    os.remove(output_path)

if __name__ == '__main__':
    main()
