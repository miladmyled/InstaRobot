import pickle
from selenium import webdriver
from time import sleep
import pymysql as mysql
import config


# Read login info from config file (JSON)

instaloginname = config.intalogin["name"]
instaloginpass = config.intalogin["pass"]

awsserver = config.awslogin["server"]
awsdatabase = config.awslogin["database"]
awsuser = config.awslogin["user"]
awspass = config.awslogin["pass"]


browser = webdriver.Chrome(".\\files\\chromedriver.exe")
browser.maximize_window()
browser.implicitly_wait(20)

#Login into insta function
def instalogin():

    # If there is a cookie for successful login it reads from in and no login is needed
    # AFTER COOKIES
    try:
        browser.get("https://www.instagram.com")
        cookies = pickle.load(open("cookies.pkl", "rb"))
        for cookie in cookies:
            browser.add_cookie(cookie)
        browser.get("https://www.instagram.com")

        not_now = browser.find_element_by_xpath("//div[@role='dialog']/div[1]/div[1]/div[3]/button[2]")

        not_now.click()
    except:
        # If cookie is not available , login is made through user and password and new cookie file will be set
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

# AWS Connection
class awslogin:
    conn = mysql.connect(
        user=awsuser, password=awspass, host=awsserver, database=awsdatabase
    )