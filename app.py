import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


service = Service(executable_path="C:\\Users\\avini\\Downloads\\Webdrivers\\chromedriver.exe")
driver = webdriver.Chrome(service=service)

csv_cols = {
    "NIT/RFP NO": "ref_no",
    "Name of Work / Subwork / Packages": "title",
    "Estimated Cost": "tender_value",
    "Bid Submission Closing Date & Time": "bid_submission_end_date",
    "EMD Amount": "emd",
    "Bid Opening Date & Time": "bid_open_date"
}


driver.get("https://etender.cpwd.gov.in/")


try:
    WebDriverWait(driver, 5).until(EC.alert_is_present())
    driver.switch_to.alert.accept()
    print("Alert accepted.")
except:
    print("No alert appeared.")


wait = WebDriverWait(driver, 10)
tender_info_tab = wait.until(EC.element_to_be_clickable((By.XPATH, '//li[@title="Tender Information"]')))
tender_info_tab.click()
time.sleep(1)
wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()='All Tenders']"))).click()
time.sleep(2)


rows = driver.find_elements(By.XPATH, "//table//tr[td]")  

data = []

for row in rows[:20]: 
    cells = row.find_elements(By.TAG_NAME, "td")
    if len(cells) >= 8:
        record = {
            "ref_no": cells[1].text.strip(),
            "title": cells[2].text.strip(),
            "tender_value": cells[4].text.strip(),
            "emd": cells[5].text.strip(),
            "bid_submission_end_date": cells[6].text.strip(),
            "bid_open_date": cells[7].text.strip(),
        }
        data.append(record)


with open("tenders.csv", "w", newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=csv_cols.values())
    writer.writeheader()
    writer.writerows(data)

print("Data saved to tenders.csv")


