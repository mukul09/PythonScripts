from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException, WebDriverException
import csv
import pandas as pd

options = webdriver.ChromeOptions()
options.add_argument("headless")
browser = webdriver.Chrome(executable_path="/home/mukul09/chromedriver")#, chrome_options=options


# To store the data in csv file
csvFile = open('Kankas_data.csv','w+')
writer = csv.writer(csvFile)
writer.writerow(('State','Licence Number','Name','Licence Type','Licence Status',
                 'License Issue Date','License Expire Date',
                 'Address','Medical School','Degree Date'))

# To get the data from the license links
def get_data(link_list):
    for i in range(len(link_list)):
        #time.sleep(1)
        #print(link_list[i])
        browser.get(link_list[i])

        state = 'Kankas'
        lic_num = WebDriverWait(browser, 100).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="agency-content"]/div[1]/div[2]/ul/li[1]'))).text.replace('License Number:', '')
        name = browser.find_element_by_xpath('//*[@id="agency-content"]/div[1]/h3').text.replace('Profile for ', '')
        #print(name)
        lic_type = 'Physician Assistant'
        lic_status = browser.find_element_by_xpath('//*[@id="agency-content"]/div[1]/div[2]/ul/li[2]').text.replace(
            'License Type:', '')

        med_school = browser.find_element_by_xpath('//*[@id="agency-content"]/div[1]/div[1]/ul/li[1]').text.replace(
            'School Name:', '')
        deg_date = browser.find_element_by_xpath('//*[@id="agency-content"]/div[1]/div[1]/ul/li[2]').text.replace(
            'Degree Date:', '')
        date_issue = browser.find_element_by_xpath('//*[@id="agency-content"]/div[1]/div[2]/ul/li[5]').text.replace(
            'Original License Date:', '')
        date_expire = browser.find_element_by_xpath('//*[@id="agency-content"]/div[1]/div[2]/ul/li[4]').text.replace(
            'License Cancellation Date:', '')
        addr = browser.find_element_by_xpath('//*[@id="agency-content"]/div[1]/div[1]/p[2]').text.replace('Address:',
                                                                                                          '')

	# Add the row in csv file
        writer.writerow((state, lic_num.strip(), name.strip(), lic_type.strip(), lic_status.strip(),
                         date_issue.strip(), date_expire.strip(), addr.strip().replace('\n', ','),med_school.strip(),
                         deg_date.strip()))

    time.sleep(1)
    back_btn = browser.find_elements_by_xpath('//*[@id="id_back"]')
    back_btn[0].click()


# To get the links of license
def get_link(tot):
    link_list = []

    for i in range(1, tot + 1):
        x = browser.find_elements_by_xpath('//*[@id="agency-content"]/table/tbody/tr[{}]/td[1]/a'.format(i))[0].get_attribute('href')
        link_list.append(x)

    get_data(link_list)


def main():
    browser.get("https://www.accesskansas.org/ssrv-ksbhada/search.html")

    lic_type = WebDriverWait(browser, 100).until(EC.presence_of_element_located((By.XPATH, '//*[@id="profession"]')))
    lic_type.send_keys('Physician Assistant')

    search_btn = WebDriverWait(browser, 100).until(EC.presence_of_element_located((By.XPATH, '//*[@id="id_submit"]')))
    search_btn.click()


    ## Get link from 1st page
    WebDriverWait(browser, 100).until(EC.presence_of_element_located((By.XPATH, '//*[@id="agency-content"]/table/tbody/tr')))
    table_trs = browser.find_elements_by_xpath('//*[@id="agency-content"]/table/tbody/tr')
    tot = len(table_trs)
    #print(tot)
    get_link(tot)



    #Check if 'NEXT' button is clickable, if yes then click and move to next page

    for i in range(1,85):
        time.sleep(2)
        buttons = browser.find_elements_by_xpath("//*[contains(text(), 'Next')]")
        #print(buttons)
        buttons[0].click()
        print('page: ',i+1)

        WebDriverWait(browser, 100).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="agency-content"]/table/tbody/tr')))
        table_trs = browser.find_elements_by_xpath('//*[@id="agency-content"]/table/tbody/tr')
        tot = len(table_trs)
        #print('total-records: ',tot)
        get_link(tot)


main()
csvFile.close()
