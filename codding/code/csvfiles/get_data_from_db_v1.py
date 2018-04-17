import json

from sqlalchemy import create_engine, MetaData, desc
from sqlalchemy.sql import select

# LANGUAGES = ['python', 'php', 'javascript', 'java', 'ruby']

engine = create_engine('sqlite:///app_information.sqlite')
connection = engine.connect()
metadata = MetaData(engine)
metadata.reflect()
db = metadata.tables['App_info']


def get_data_from_db(db):
    selection = select([db.c.app_name, db.c.viewed_number])
    selection = selection.order_by(desc(db.c.posted_time))
    selection = selection.limit(100)
    result_proxy = connection.execute(selection)
    app_infos = result_proxy.fetchall()
    column_name = result_proxy.keys()
    return app_infos, column_name
    # for item in app_infos:
    #     print(type(item))
    #     print(item)


def generate_first_json_file(processed_data):
    with open('first_json_file.json', 'w+', encoding='utf-8') as f:
        f.write(json.dumps(processed_data) + '\n')

def process_data(data):
    # 从前100个应用中剔除掉浏览量低于100的应用
    data = [item for item in data[0] if item[1] > 100]
    # 应用名
    app_name = [item[0].lower() for item in data]
    # 应用的浏览量
    app_viewed_number = [item[1] for item in data]
    raw_list = list(zip(app_name, app_viewed_number))
    # clean up the duplicating data if exist.
    processed_data = set(raw_list)
    processed_data = list(processed_data)
    # 对数据按照浏览量由大到小进行排序
    processed_data.sort(key=lambda x: x[1], reverse=True)
    # the length of processed data
    return processed_data


if __name__ == "__main__":
    data = get_data_from_db(db)
    processed_data = process_data(data)
    generate_first_json_file(processed_data)
