import sqlite3
import json

conn = sqlite3.connect('app_information.sqlite')
cur = conn.cursor()

cur.execute('SELECT app_name, viewed_number, url, posted_time FROM App_info')

a = cur.fetchall()


# for item in a:
#     print(item[0], item[1], '\n')
b = json.dumps(a)


with open('app_name_and_viwed_number.json', 'w', encoding='utf-8') as f:
    f.write(b)


print(a)
print(b)
