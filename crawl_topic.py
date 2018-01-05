import requests
import json
from lxml import etree
import pymysql


def get_conn():
    db_conn = pymysql.connect(
        host="localhost",
        db="zhihu",
        user="root",
        passwd="123456",
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor
    )
    return db_conn


def close_conn(db_conn):
    db_conn.close()


def topic(offset):
    url = 'https://www.zhihu.com/topic/20011035/newest'
    data = {
        "start": 0,
        "offset": offset
    }
    response = session.post(url, data=data, headers=headers)
    response_json = json.loads(response.text)
    if response_json['msg'][0] <= 0:
        print('no data...')
        return
    html = etree.HTML(response_json['msg'][1])
    items = html.xpath('//div[starts-with(@class, "feed-item")]')
    sql = 'insert ignore into t_zhihu_topic_question(topic_id, question_id, question_name) values'
    for item in items:
        data_score = item.xpath('./@data-score')
        question_ids = item.xpath('./div[@class="feed-main"]/div/h2/a/@href')
        question_names = item.xpath('./div[@class="feed-main"]/div/h2/a/text()')
        if len(question_ids) > 0 and len(question_names) > 0:
            sql += "(20011035, "+question_ids[0].split("/")[2]+", '"+question_names[0].replace('\n', '')+"'),"

    sql = sql[:len(sql)-1]

    db_conn = get_conn()
    with db_conn.cursor() as cursor:
        cursor.execute(sql)
        db_conn.commit()
    print(data_score)
    topic(data_score)


if __name__ == '__main__':
    session = requests.session()
    headers = {
        "Host": "www.zhihu.com",
        "Referer": "https://www.zhihu.com/",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/63.0.3239.84 Safari/537.36"
    }
    topic(1513348009.00000)
