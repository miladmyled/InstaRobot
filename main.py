from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import login
from datetime import datetime

# Defining main hashtags and second related hashtags
mainTags = ['vancouver', 'britishcolumbia', 'vancity', 'northvancouver', 'bc', 'burnaby', 'coquitlam', 'Abbotsford',
            'yvr', \
            'vancouverbc', 'surrey', 'vancitybuzz', 'vancouverisawesome', 'langley', 'vancityhype', 'newwestminster',
            'vancouverfoodie', \
            'eastvan', 'yvreats', 'kelowna', 'vancouverisland', 'vancouverlife']
# mainTags = ['vancouver', 'britishcolumbia', 'vancity']


searchTags = ['wine', 'beer', 'whiskey', 'vodka', 'sparklingwine', 'champagne', 'tequila']
# Login to AWS
conn = login.awslogin.conn
cursor = conn.cursor


# Create Error Log Function
def logerror(functionname, errortext):
    sqltext = "INSERT INTO logs (function, errortext) VALUES (%s, %s)"
    values = (functionname, errortext)
    cursor.execute(sqltext, values)
    conn.commit()


# Login in Instagram
try:
    login.instalogin()
except Exception as e:
    logerror("instalogin", e)


# Open Chrome Driver
browser = webdriver.Chrome(".\\files\\chromedriver.exe")
browser.maximize_window()
browser.implicitly_wait(20)




hreflist = []

# Search Each hashtag, scroll down te page to load more posts for 20 times and read href of each post from 5 posts in
# a column and 3 in a row
for x in mainTags:
    try:
        browser.get('https://www.instagram.com/explore/tags/' + x)
        browser.find_element_by_tag_name('body').send_keys(Keys.HOME)
        browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        sleep(3)
    except Exception as e:
        logerror("main tags search", e)
    for a in range(20):
        # for a in range(5):
        try:
            browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            sleep(3)
        except Exception as e:
            logerror("Scroll down", e)
        for i in range(5):
            # for i in range(1):
            for j in range(3):
                try:
                    post = browser.find_element_by_xpath(
                        "//div[@id='react-root']/section/main/article/div[2]/div[1]/div[" + str(i + 1) + "]/div[" + str(
                            j + 1) + "]/a")
                    hreflist.append(post.get_attribute("href"))
                except Exception as e:
                    logerror("element not attached", e)
                    print("element not attached")

# Save all hrefs in a list and make them unique
hreflist = list(set(hreflist))
finalhreflist = []
lenhreflist = len(list(set(hreflist)))
print(lenhreflist)

# Open each post and see if related keywords exist in post's caption or not , if exists save it in final list
for hrf in hreflist:
    browser.get(hrf)
    sleep(1)
    try:
        post_text = browser.find_element_by_xpath(
            "//div[@id='react-root']/section/main/div[1]/div[1]/article/div[2]/div[1]/ul/div[1]/li/div[1]/div[1]/div[2]/span").text
        for st in searchTags:
            if st in post_text:
                finalhreflist.append(hrf)
    except Exception as e:
        logerror('search tag post not available', e)
        print('page not available')
        sleep(30)
    print(lenhreflist)
    lenhreflist -= 1

# Make final list unique and save it to a text file
finalhreflist = list(set(finalhreflist))
print(len(list(set(finalhreflist))))
with open('result.txt', 'w') as f:
    for item in finalhreflist:
        f.write("%s\n" % item)

# Open each post on final list , go to the profile check if the profile exists in database or not , if not
# follow it and save profile name , href and datetime in the database
for fhrf in finalhreflist:
    browser.get(fhrf)
    sleep(2)
    try:
        profile_address = browser.find_element_by_xpath(
            "//div[@id='react-root']/section/main/div[1]/div[1]/article/header/div[2]/div[1]/div[1]/a").get_attribute(
            "href")
        cursor.execute('select (1) from followings where href = "' + profile_address + '" limit 1')
    except Exception as e:
        logerror("profile address not found" , e)
    msg = cursor.fetchone()
    # check if it is empty
    if not msg:
        browser.get(profile_address)
        sleep(2)
        try:
            follow_btn = browser.find_element_by_xpath(
                "//div[@id='react-root']/section/main/div[1]/header/section/div[1]/div[1]/span/span/button")
            profile_name = browser.find_element_by_xpath(
                "//div[@id='react-root']/section/main/div[1]/header/section/div[1]/h2").text
            sql = "INSERT INTO followings (profile_name, href , updated_date , is_followed) VALUES (%s, %s, %s, %s)"
            val = (profile_name, profile_address, datetime.now(), 1)
            cursor.execute(sql, val)
            conn.commit()
            follow_btn.click()
        except Exception as e:
            logerror("follow not available" , e)
            print("follow not available")
