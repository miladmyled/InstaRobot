from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import login
from datetime import datetime



mainTags = ['vancouver', 'britishcolumbia', 'vancity', 'northvancouver', 'bc', 'burnaby', 'coquitlam', 'Abbotsford', 'yvr', \
            'vancouverbc', 'surrey', 'vancitybuzz', 'vancouverisawesome', 'langley', 'vancityhype', 'newwestminster', 'vancouverfoodie', \
            'eastvan', 'yvreats', 'kelowna', 'vancouverisland', 'vancouverlife']
# mainTags = ['vancouver', 'britishcolumbia', 'vancity']


searchTags = ['wine', 'beer', 'whiskey', 'vodka', 'sparklingwine', 'champagne', 'tequila']

login.instalogin()

browser = webdriver.Chrome(".\\files\\chromedriver.exe")
browser.maximize_window()
browser.implicitly_wait(20)

conn = login.awslogin.conn
cursor = conn.cursor

hreflist = []


for x in mainTags:
    browser.get('https://www.instagram.com/explore/tags/' +x)
    browser.find_element_by_tag_name('body').send_keys(Keys.HOME)
    browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    sleep(3)
    for a in range(20):
    # for a in range(5):
        browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        sleep(3)
        for i in range(4):
        # for i in range(1):
            for j in range(3):
                try:
                    post = browser.find_element_by_xpath(
                        "//div[@id='react-root']/section/main/article/div[2]/div[1]/div[" + str(i + 1) + "]/div[" + str(
                            j + 1) + "]/a")
                    hreflist.append(post.get_attribute("href"))
                except:
                    print("element not attached")

hreflist = list(set(hreflist))
finalhreflist = []
lenhreflist = len(list(set(hreflist)))
print(lenhreflist)

for hrf in hreflist:
    browser.get(hrf)
    sleep(1)
    try:
        post_text = browser.find_element_by_xpath(
            "//div[@id='react-root']/section/main/div[1]/div[1]/article/div[2]/div[1]/ul/div[1]/li/div[1]/div[1]/div[2]/span").text
        for st in searchTags:
            if st in post_text:
                finalhreflist.append(hrf)
    except:
        print('page not available')
        sleep(30)
    print(lenhreflist)
    lenhreflist -= 1

finalhreflist = list(set(finalhreflist))
print(len(list(set(finalhreflist))))
with open('result.txt', 'w') as f:
    for item in finalhreflist:
        f.write("%s\n" % item)

for fhrf in finalhreflist:
    browser.get(fhrf)
    sleep(2)
    profile_address = browser.find_element_by_xpath(
        "//div[@id='react-root']/section/main/div[1]/div[1]/article/header/div[2]/div[1]/div[1]/a").get_attribute("href")
    cursor.execute('select (1) from followings where href = "' + profile_address + '" limit 1')
    msg = cursor.fetchone()
    # check if it is empty and print error
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
        except:
            print("follow not available")