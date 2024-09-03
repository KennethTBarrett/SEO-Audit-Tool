import subprocess
import json
import tempfile
import os

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