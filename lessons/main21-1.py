from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(url='https://quasarzone.com/bbs/qb_saleinfo')
driver.implicitly_wait(time_to_wait=10)
titles = driver.find_elements(By.CLASS_NAME, 'ellipsis-with-reply-cnt')
urls = driver.find_elements(By.CLASS_NAME, 'tit')

for i in range(len(titles)):
    print(titles[i].text)
    print(urls[i].get_attribute('href'))

while True:
    pass
