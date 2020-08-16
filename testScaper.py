from bs4 import BeautifulSoup
import requests

url = "http://www.google.com/search?q=shakespeare+pdf"
get = requests.get(url).text
soup = BeautifulSoup(get)

urls = soup.findAll('div', attrs={'class':'kCrYT'})
print(urls)