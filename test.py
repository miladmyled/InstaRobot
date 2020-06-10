import login
from time import sleep
from datetime import datetime

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

finalhreflist = []
with open('result.txt') as my_file:
    for line in my_file:
        line = line[:-2]
        finalhreflist.append(line)


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
        if follower_count < 1000 :
            try:
                follow_btn = login.browser.find_element_by_xpath(
                    "//div[@id='react-root']/section/main/div[1]/header/section/div[1]/div[1]/span/span/button")
                profile_name = login.browser.find_element_by_xpath(
                    "//div[@id='react-root']/section/main/div[1]/header/section/div[1]/h2").text
                sql = "INSERT INTO followings (profile_name, href , updated_date , is_followed) VALUES (%s, %s, %s, %s)"
                val = (profile_name, profile_address, datetime.now(), 1)
                with conn.cursor() as cursor:
                    cursor.execute(sql, val)
                conn.commit()
                follow_btn.click()
            except Exception as e:
                print(e)
                logerror("follow not available" , e)
        elif following_count >= 1000:
            try:
                followers_btn = login.browser.find_element_by_xpath(
                    "//div[@id='react-root']/section/main/div[1]/header/section/ul/li[2]/a")
                followers_btn.click()
                for a in range(20):
                    # for a in range(5):
                    try:
                        login.browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                        sleep(2)
                    except Exception as e:
                        print(e)
                        logerror("Scroll down followers section", e)
                #for f in range(20)
                profile_name = login.browser.find_element_by_xpath(
                    "//div[@id='react-root']/section/main/div[1]/header/section/div[1]/h2").text
                sql = "INSERT INTO followings (profile_name, href , updated_date , is_followed) VALUES (%s, %s, %s, %s)"
                val = (profile_name, profile_address, datetime.now(), 1)
                with conn.cursor() as cursor:
                    cursor.execute(sql, val)
                conn.commit()
                follow_btn.click()
            except Exception as e:
                print(e)
                logerror("follow not available" , e)

