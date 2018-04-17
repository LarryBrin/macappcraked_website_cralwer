import sqlite3

conn = sqlite3.connect('store_item.sqlite')

cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS App_info (title text,
            meta_info text, time text, viewed_numbers text, url text)''')
with open('./meta_info.csv', 'rt', encoding='utf-8') as f:
    for line in f:
        # print(line)
        items = line.split(',', maxsplit=4)
        title, meta_info, posted_time, viewed_numbers, url = tuple(items)
        cur.execute('INSERT INTO App_info VALUES (?, ?, ?, ?, ?)',
                    (title, meta_info, posted_time, viewed_numbers, url))
    conn.commit()
    cur.close()
