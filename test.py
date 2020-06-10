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


login.browser.get('https://www.instagram.com/capsliquor/')
followers_btn = login.browser.find_element_by_xpath(
                    "//div[@id='react-root']/section/main/div[1]/header/section/ul/li[2]/a")
followers_btn.click()
for a in range(20):
    # for a in range(5):
    try:
        fBody = login.browser.find_element_by_xpath("//div[@class='isgrP']")
        login.browser.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;',                                     fBody)
        sleep(2)
    except Exception as e:
        print(e)
        logerror("Scroll down followers section", e)
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

