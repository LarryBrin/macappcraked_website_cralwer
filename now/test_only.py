import csv
with open('eggs.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(['Spam'] * 5 + ['Baked Beans'])
    spamwriter.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])





import csv
titles = ['1', '2', '3', '4', '5']
num = [1, 2, 3, 4, 5]
asc = ['a', 'b', 'c', 'd', 'e']
data = list(zip(titles, num, asc))
for datum in data:
    # print(datum)

# for datum in data:
# d = lambda x: for datum in data
# print(d)
# print(d)
# print(data)
with open('csvfil.csv', 'w', encoding='UTF-8') as csvfil:
    handler = csv.writer(item for item in csvfil)
    handler.writerow()




import os.path

Bool = os.path.exists('./pages_sources/htmlfiles/main_pages')
print(Bool)


titles = 'fiewif mdiwmi fwie – fmw mwo 21304'
# print(titles.split('–'))


def test(st):
    titles =[]
    meta_infos = []
    title_item = st.split('–')
    titles.append(title_item[0])
    meta_infos.append(title_item[1])
    return titles, meta_infos


you = test(titles)
print(you)

# import csv











for a, c in titles, asc:
    print(a, c)
