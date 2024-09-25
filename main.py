from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep

USERNAME='TypeYourUsernameHere'
PASSWORD='TypeYourPasswordHere'

USERNAME = input('Type your username:')
PASSWORD = input('Type your password:')

def claims2dicts(page_source):

    page = BeautifulSoup(page_source)
    table = page.find('table')

    data=[]
    for row in table.find_all('tr')[1:]:  # Skip the header row
        cols = row.find_all('td')
        if len(cols) > 8:  # Check if there are columns
            entry = {
                'Reference': cols[1].text.strip(),
                'Created By': cols[2].text.strip(),
                'Created Date': cols[3].text.strip(),
                'Delivered From': cols[4].text.strip(),
                'Delivered To': cols[5].text.strip(),
                'Case Notes': cols[6].text.strip(),
                'Total Amount': cols[7].text.strip(),
                'Status': cols[8].text.strip()
            }
            data.append(entry)
    return data

def invoices2dicts(page_source):

    page = BeautifulSoup(page_source)
    table = page.find('table')

    data=[]
    for row in table.find_all('tr')[1:]:  # Skip the header row
        cols = row.find_all('td')
        if len(cols) > 6:  # Check if there are columns
            entry = {
                'Extraction Date': cols[1].text.strip(),
                'Services Delivered From': cols[2].text.strip(),
                'Services Delivered To': cols[3].text.strip(),
                'Num Delivered Services': cols[4].text.strip(),
                'Delivered To': cols[5].text.strip(),
                'Status': cols[6].text.strip()
            }
            data.append(entry)
    return data


def dicts2excel(dicts, output_file='data.xlsx'):

    df = pd.DataFrame(dicts)
    df.to_excel(output_file, index=False)

def main():
    driver = webdriver.Chrome()

    driver.get(r'https://app.careview.io/login')

    #Login
    username = driver.find_element(By.ID, 'txtUsername')  
    password = driver.find_element(By.ID, 'txtPassword')  
    username.send_keys(USERNAME)  
    password.send_keys(PASSWORD)    
    login_button = driver.find_element(By.ID, 'btnLogin')  
    login_button.click()

    sleep(3)

    #Check for Verification Code
    try:
        access_code = driver.find_element(By.ID, 'txtAccessCode')

        print('Access code is required, please check your email for access code and type it here:')
        access_code.send_keys(input())
    except:
        try:
            driver.find_element(By.ID, 'txtUsername') 
            print('Invalid Email or password')
            return
        except:
            print('No access code required.')
            print('Logged in Successfully')

    #Convert Claims
    driver.find_element(By.LINK_TEXT, 'AH invoices').click()
    sleep(2)
    page_source = driver.page_source

    data = claims2dicts(page_source)
    dicts2excel(data, 'claims.xlsx')

    #Convert Reports
    driver.find_element(By.LINK_TEXT, 'AH NDIS invoices').click()
    sleep(2)
    page_source = driver.page_source

    data = invoices2dicts(page_source)
    dicts2excel(data, 'invoices.xlsx')


if __name__=='__main__':
    main()