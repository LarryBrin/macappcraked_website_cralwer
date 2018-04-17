main_page_info = main_page_items('./htmlfiles/main_pages/2018-01-30 15/36/07.html')  # 调用 main_apge_tiems 函数.
  titles = main_page_info[0]
  home_page_items_number = len(titles)  # 抓页面条目数量，为确定后续抓取切入点作准备
  for title in titles:
      if '+' in title:
          title_split_raw = title.rsplit(sep='+', maxsplit=1)[0].strip()
          title_split = title_split_raw.rsplit(sep=' ', maxsplit=1)
      else:
          title_split = title.rsplit(sep=' ', maxsplit=1)
      app_name = title_split[0]
      version_str = title_split[1].strip()
      dot_split = version_str.split('.')
      try:
          version_list = [int(item) for item in dot_split]
      except ValueError:
          version_list = []
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
      # try:
      #     version_list = {int(item) for item in app_version_str}
      # except ValueError:
      #     version_list = {item for item in app_version_str}
      if app_name not in already_stored_items:
          # print('have not stored app_name: %s\n' % app_name)
          new_titles.append(title)
          new_crawled_item_number += 1
      elif app_name in already_stored_items and version_list > already_stored_items[app_name]:
          # print('already_stored_items but upgraded: %s\n' % app_name)
          # print('version: ', already_stored_items[app_name])
          new_titles.append(title)
          new_crawled_item_number += 1
      elif app_name in already_stored_items and version_list < already_stored_items[app_name]:
          # print('already_stored_items and version is lower: %s\n' % app_name)
          # print('version: ', already_stored_items[app_name])
          new_crawled_item_number += 1
      elif app_name in already_stored_items and version_list == already_stored_items[app_name]:
          jump_to_page_havent_been_crawled = True

  # 根据上述判断开始爬取未爬取的应用条目
  should_be_crawled_items_number = len(new_titles)
  app_urls = main_page_info[-1][:should_be_crawled_items_number]
  urls = get_item_details(app_urls, new_titles)
  meta_infos = main_page_info[1]
  times = main_page_info[2]
  viewed_numbers = main_page_info[3]
  contents = main_page_info[-2]
  current_app_num = previously_crawled_number + new_crawled_item_number
  data = list(zip(new_titles, meta_infos, viewed_numbers,
                  times, urls, contents))

  # 存储本地数据
  generate_scv_file(data)
  storing_data_in_db(data, current_app_num)

  # 判断是连续爬取还是跳转爬取
  try:
      if jump_to_page_havent_been_crawled:
          # url = start_url(start_num)
          have_been_crawed_items_number = previously_crawled_number + new_crawled_item_number
          page_number = math.floor(have_been_crawed_items_number / home_page_items_number)
  except :
      pass
  # page_number += 1
  # url = start_url(page_number)
  # crawling(already_stored_items, previously_crawled_number,
  #          page_number=page_number,
  #          url=url,
  #          new_crawled_item_number=new_crawled_item_number)
