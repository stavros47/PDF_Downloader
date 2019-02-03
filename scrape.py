import math
import re #regular expressions
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm #progress bar library


def downloadFile(url, fileName):
    fileResult = requests.get(url, stream=True)
    # Total size in bytes.
    total_size = int(fileResult.headers.get('content-length', 0)); 
    block_size = 1024
    wrote = 0
   
    with open(fileName, "wb+") as file:
        for data in tqdm(fileResult.iter_content(block_size), desc='Progress', total=math.ceil(total_size//block_size) , unit='KB', unit_scale=True):
            wrote = wrote  + len(data)
            file.write(data)
    if total_size != 0 and wrote != total_size:
        print("ERROR, something went wrong!") 

url = "https://www.csd.uoc.gr/~hy360/2018/"
result = requests.get("https://www.csd.uoc.gr/~hy360/2018/assignments.html",stream=True)
result.encoding = 'utf-8'
#print(result.status_code)
#print(result.headers)

src = result.content
soup = BeautifulSoup(src, 'lxml')
links = soup.find_all(href=re.compile('.+\.pdf$'))

for link in links:
    file_url = url + link.attrs['href']    
  
    #https://stackoverflow.com/questions/18727347/how-to-extract-a-filename-from-a-url-append-a-word-to-it
    fileName = file_url[file_url.rfind("/")+1:]
    print("\n"+fileName)   
    downloadFile(file_url, fileName)
    