import re

with open('./meta_info.csv', 'r+', encoding="UTF-8") as f:
    import re
    app_items = {}
    app_num = 0
    total = re.findall(',(.*?)$', f.read())
    pattern = re.compile('"?(.*?[0-9].*?)"?,')
    for line in f:
        # print(line)
        title = pattern.findall(line)[0]
        # print(type(line))
        # print(line)
        if '+' in title:
            title_split_raw = title.rsplit(sep='+', maxsplit=1)[0].strip()
            title_split = title_split_raw.rsplit(sep=' ', maxsplit=1)
        else:
            title_split = title.rsplit(sep=' ', maxsplit=1)
        # print(title_split)
        version_str = title_split[1].strip()
        dot_split = version_str.split('.')
        # if not dot_split[0]
        try:
            version_list = [int(item) for item in dot_split]
        except ValueError:
            version_list = []
            # version_list = [item for item in dot_split]
            # version_list_raw = re.findall('([a-z]*?)([0-9]*?)', version_str)
            for item in dot_split:
                try:
                    item = int(item)
                    version_list.append(item)
                except ValueError:
                    raw = re.findall('([a-z]{1,})|([0-9]{1,})', item)
                    for item in raw:
                        item1, item2 = item
                        if item1 == '':
                            version_list.append(int(item2))
                        if item2 == '':
                            version_list.append(item1)
                    # raw_num = re.findall('([0-9]{1,})')
        # print(version_list)
        # for item in version_list:
        #     if isinstance(item, str):
        #         print(version_list)
                # print(line)
        app_items[title_split[0]] = version_list
        app_num += 1
        print(total)
