from time import sleep
from selenium.webdriver.common.keys import Keys
import login
from datetime import datetime




# Defining main hashtags and second related hashtags
mainTags = ['vancouver', 'britishcolumbia', 'vancity', 'northvancouver', 'bc', 'burnaby', 'coquitlam', 'Abbotsford', 'yvr', 'vancouverbc', 'surrey', 'vancitybuzz', 'vancouverisawesome', 'langley', 'vancityhype', 'newwestminster', 'vancouverfoodie', 'eastvan', 'yvreats', 'kelowna', 'vancouverisland', 'vancouverlife']
# mainTags = ['vancouver', 'britishcolumbia', 'vancity']


searchTags = ['wine', 'beer', 'whiskey', 'vodka', 'sparklingwine', 'champagne', 'tequila']
# Login to AWS
conn = login.awslogin.conn


# Create Error Log Function
def logerror(functionname, errortext):
    with conn.cursor() as cursor:
        # Create a new record
        sqltext = "INSERT INTO errorlogs (error_topic, errortext) VALUES (%s, %s)"
        errortext = str(errortext).replace("'", "")
        cursor.execute(sqltext, (functionname, errortext))
    # connection is not autocommit by default. So you must commit to save
    # your changes.
    conn.commit()


# Login in Instagram
try:
    login.instalogin()
except Exception as e:
    logerror("instalogin", e)




hreflist = []

# Search Each hashtag, scroll down te page to load more posts for 20 times and read href of each post from 5 posts in
# a column and 3 in a row
for x in mainTags:
    try:
        login.browser.get('https://www.instagram.com/explore/tags/' + x)
        login.browser.find_element_by_tag_name('body').send_keys(Keys.HOME)
        login.browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        sleep(3)
    except Exception as e:
        print(e)
        logerror("main tags search", e)
    for a in range(20):
        # for a in range(5):
        try:
            login.browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            sleep(3)
        except Exception as e:
            print(e)
            logerror("Scroll down", e)
        for i in range(5):
            # for i in range(1):
            for j in range(3):
                try:
                    post = login.browser.find_element_by_xpath(
                        "//div[@id='react-root']/section/main/article/div[2]/div[1]/div[" + str(i + 1) + "]/div[" + str(
                            j + 1) + "]/a")
                    hreflist.append(post.get_attribute("href"))
                except Exception as e:
                    print(e)
                    logerror("element not attached", e)

# Save all hrefs in a list and make them unique
hreflist = list(set(hreflist))
finalhreflist = []
lenhreflist = len(list(set(hreflist)))
print(lenhreflist)

# Open each post and see if related keywords exist in post's caption or not , if exists save it in final list
for hrf in hreflist:
    login.browser.get(hrf)
    sleep(1)
    try:
        post_text = login.browser.find_element_by_xpath(
            "//div[@id='react-root']/section/main/div[1]/div[1]/article/div[2]/div[1]/ul/div[1]/li/div[1]/div[1]/div[2]/span").text
        for st in searchTags:
            if st in post_text:
                finalhreflist.append(hrf)
    except Exception as e:
        print(e)
        logerror('search tag post not available', e)
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
    login.browser.get(fhrf)
    sleep(2)
    try:
        profile_address = login.browser.find_element_by_xpath(
            "//div[@id='react-root']/section/main/div[1]/div[1]/article/header/div[2]/div[1]/div[1]/a").get_attribute(
            "href")
        with conn.cursor() as cursor:
            cursor.execute('select (1) from followings where href = "' + profile_address + '" limit 1')
    except Exception as e:
        print(e)
        logerror("profile address not found" , e)
    msg = cursor.fetchone()
    # check if it is empty
    if not msg:
        login.browser.get(profile_address)
        try:
            follower_count = int(login.browser.find_element_by_xpath(
                "//div[@id='react-root']/section/main/div[1]/header/section/ul/li[2]/a/span").text)
            following_count = int(login.browser.find_element_by_xpath(
                "//div[@id='react-root']/section/main/div[1]/header/section/ul/li[3]/a/span").text)
        except :
            follower_count = 1001
            following_count = 1001
        sleep(2)
        if follower_count < 1000:
            try:
                follow_btn = login.browser.find_element_by_xpath(
                    "//div[@id='react-root']/section/main/div[1]/header/section/div[1]/div[1]/span/span/button")
                profile_name = login.browser.find_element_by_xpath(
                    "//div[@id='react-root']/section/main/div[1]/header/section/div[1]/h2").text

                sql = "INSERT INTO followings (profile_name, href , updated_date , is_followed) VALUES (%s, %s, %s, %s)"
                val = (profile_name, profile_address, datetime.now(), 0)
                with conn.cursor() as cursor:
                    cursor.execute(sql, val)
                conn.commit()
                #follow_btn.click()
            except Exception as e:
                print(e)
                logerror("follow not available" , e)
        elif follower_count >= 1000:
            try:
                followers_btn = login.browser.find_element_by_xpath(
                    "//div[@id='react-root']/section/main/div[1]/header/section/ul/li[2]/a")
                followers_btn.click()
                for a in range(20):
                    # for a in range(5):
                    try:
                        fBody = login.browser.find_element_by_xpath("//div[@class='isgrP']")
                        login.browser.execute_script(
                            'arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;',
                            fBody)
                        sleep(2)
                        for f in range(100):
                            profile_name = login.browser.find_element_by_xpath(
                                "//div[@role='dialog']/div[1]/div[2]/ul/div[1]/li[" + str(f + 1) + "]/div[1]/div[1]/div[2]/div[1]/a").text
                            href = 'https://www.instagram.com/' + profile_name
                            with conn.cursor() as cursor:
                                cursor.execute(
                                    "select (1) from followings WHERE href LIKE  '%" + profile_name + "%' limit 1")
                            msg = cursor.fetchone()
                            # check if it is empty
                            if not msg:
                                sql = "INSERT INTO followings (profile_name, href , updated_date , is_followed) VALUES (%s, %s, %s, %s)"
                                val = (profile_name, href, datetime.now(), 0)
                                with conn.cursor() as cursor:
                                    cursor.execute(sql, val)
                                conn.commit()
                    except Exception as e:
                        print(e)
                        logerror("Scroll down followers section", e)
            except Exception as e:
                print(e)
                logerror("follow not available" , e)
