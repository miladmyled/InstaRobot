# Login to AWS
conn = login.awslogin.conn
cursor = conn.cursor


sql = "INSERT INTO followings (profile_name, href , updated_date , is_followed) VALUES (%s, %s, %s, %s)"
val = (profile_name, profile_address, datetime.now(), 1)
cursor.execute(sql, val)
conn.commit()