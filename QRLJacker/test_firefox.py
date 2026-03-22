from selenium import webdriver
from selenium.webdriver.firefox.options import Options

try:
    print("Initializing Firefox options...")
    options = Options()
    options.headless = True
    print("Starting webdriver.Firefox()...")
    driver = webdriver.Firefox(options=options)
    print("Success! Firefox started.")
    driver.quit()
except Exception as e:
    print(f"Failed: {e}")
