from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import time
import shutil

print("Starting Firefox...")
opts = Options()
# Let's run it visible so the user can see what's happening and scan it manually during the test
opts.headless = False 

gecko = shutil.which('geckodriver') or '/usr/local/share/geckodriver'
driver = webdriver.Firefox(options=opts, executable_path=gecko)

print("Navigating to WhatsApp Web...")
driver.get("https://web.whatsapp.com")

print("Please scan the QR code in the Firefox window that just opened.")
print("Waiting 30 seconds for you to scan and login...")
time.sleep(30)

print("Checking for session identifiers...")

identifiers_to_test = [
    ('ID pane-side', '//div[@id="pane-side"]'),
    ('Data-testid chat-list', '//div[@data-testid="chat-list"]'),
    ('Header avatar', '//header//img'),
    ('Search input', '//div[@contenteditable="true"][@data-tab="3"]')
]

found_any = False
for name, xpath in identifiers_to_test:
    try:
        element = driver.find_element(By.XPATH, xpath)
        if element:
            print(f"[SUCCESS] Found {name}: {xpath}")
            found_any = True
    except:
        print(f"[FAILED] Could not find {name}: {xpath}")

if not found_any:
    print("\n[WARNING] Could not find any standard post-login elements. The DOM might be entirely different.")
    print("Dumping a snippet of the current body HTML for analysis...")
    body = driver.find_element(By.TAG_NAME, "body").get_attribute("innerHTML")
    print(body[:1000])

driver.quit()
print("Done.")
