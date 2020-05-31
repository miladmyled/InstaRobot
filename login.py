import pickle
from selenium import webdriver
from time import sleep
import pymysql as mysql
import json

infolist = []
with open('info.config', 'r') as f:
    for line in f:
        infolist.append(line)
instalogininfo = json.loads(infolist[0])
instaloginname = instalogininfo["name"]
instaloginpass = instalogininfo["pass"]
awslogininfo = json.loads(infolist[1])
awsserver = awslogininfo["server"]
awsdatabase = awslogininfo["database"]
awsuser = awslogininfo["user"]
awspass = awslogininfo["pass"]




def instalogin():
    browser = webdriver.Chrome(".\\files\\chromedriver.exe")
    browser.maximize_window()
    browser.implicitly_wait(20)


    # AFTER COOKIES
    try:
        browser.get("https://www.instagram.com")
        cookies = pickle.load(open("cookies.pkl", "rb"))
        for cookie in cookies:
            browser.add_cookie(cookie)
        browser.get("https://www.instagram.com")

        not_now = browser.find_element_by_xpath("//div[@role='dialog']/div[1]/div[3]/button[2]")

        not_now.click()
    except:
        #Save Cookies
        browser.get('https://www.instagram.com/accounts/login/')
        user_name = browser.find_element_by_xpath("//div[@id='react-root']/section/main/div[1]/article/div[1]/div[1]/div["
                                                  "1]/form/div[2]/div[1]/label/input")

        password = browser.find_element_by_xpath("//div[@id='react-root']/section/main/div[1]/article/div[1]/div[1]/div["
                                                 "1]/form/div[3]/div[1]/label/input")

        login = browser.find_element_by_xpath("//div[@id='react-root']/section/main/div[1]/article/div[1]/div[1]/div[1]/form/div[4]/button")

        sleep(1)
        user_name.click()
        user_name.send_keys(instaloginname)
        password.click()
        password.send_keys(instaloginpass)
        sleep(1)
        login.click()
        sleep(20)
        pickle.dump(browser.get_cookies(), open("cookies.pkl", "wb"))
        browser.get("https://www.instagram.com")

        not_now = browser.find_element_by_xpath("//div[@role='dialog']/div[1]/div[3]/button[2]")

        not_now.click()

def awslogin():
    conn = mysql.connect(
        user=awsuser, password=awspass, host=awsserver, database=awsdatabase
    )
    cursor = conn.cursor()