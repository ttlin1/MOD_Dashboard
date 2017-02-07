from bs4 import BeautifulSoup
import requests
import os
import urllib

html_string = "http://trimet.org/about/dashboard/index.htm"
html_doc = requests.get(html_string)
soup = BeautifulSoup(html_doc.text, 'html.parser')

links = []
for link in soup.find_all('link'):
    links.append(link.get('href'))

root_dir = r"G:\PUBLIC\LinT\MOD_Sandbox_Dashboard\webpage"
for l in links:
    try:
        urllib.urlretrieve(html_string + l, os.path.join(root_dir + l))
    except:
        print l
