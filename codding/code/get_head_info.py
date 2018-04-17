from requests import Session
# from the_zero_page import response

url = 'https://nmac.to/page/680'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) \
               AppleWebKit/537.36 (KHTML, like Gecko) \
               Chrome/65.0.3311.3 Safari/537.36'}
session = Session()
res = session.get(url, headers=headers)
with open('header.txt', 'w+') as head:
    state = res.status_code
    stat = res.encoding
    text = res.headers
    print(text, stat, state)
    for item in text:
        head.write(item + ": " + text[item] + "\n")

with open('res.html', 'w+', encoding='UTF-8') as h:
    h.writelines(res.text)·
