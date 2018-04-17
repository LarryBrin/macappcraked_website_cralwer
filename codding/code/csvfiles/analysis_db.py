import sqlite3
import os
import os.path

db_parh = os.path.join(os.getcwd(), 'app_information.sqlite')
print(db_parh)

with sqlite3.connect(db_parh) as conn:

    cur = conn.cursor()

    cur.execute('SELECT viewed_number, posted_time FROM App_info')

    a = cur.fetchall()
    a1 = cur.fetchone()
    print(a)
