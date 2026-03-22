from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
from bs4 import BeautifulSoup
from lxml import etree

opts = Options()
opts.headless = True
driver = webdriver.Firefox(options=opts)
driver.get("https://web.whatsapp.com")
time.sleep(5)
html = driver.page_source
driver.quit()

soup = BeautifulSoup(html, "html.parser")
canvas = soup.find("canvas")
if canvas:
    print("Found canvas!")
    dom = etree.HTML(str(soup))
    print("XPath:", dom.getpath(dom.xpath('//canvas')[0]))
else:
    print("No canvas found. Page might be blocking headless browsers or loading slowly.")
