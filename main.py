import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
def download_files(url, num_files):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    files = [urljoin(url, a['href']) for a in soup.find_all('a', href=True)]
    files = [file for file in files if file.endswith(('.jpg', '.jpeg', '.png', '.gif', '.txt', '.pdf'))]
    files.sort(key=lambda x: urlparse(x).path)

    download_dir = 'downloads'
    os.makedirs(download_dir, exist_ok=True)

    for i, file in enumerate(files[:num_files]):
        print(f'Downloading file {i+1} of {num_files}: {file}')
        response = requests.get(file, stream=True)
        filename = os.path.basename(urlparse(file).path)
        filepath = os.path.join(download_dir, filename)
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)

    middle_index = len(files) // 2
    for i, file in enumerate(files[middle_index:middle_index+num_files]):
        print(f'Downloading middle file {i+1} of {num_files}: {file}')
        response = requests.get(file, stream=True)
        filename = os.path.basename(urlparse(file).path)
        filepath = os.path.join(download_dir, filename)
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
download_files('', 50)