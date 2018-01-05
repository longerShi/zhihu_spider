import requests
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


def get_question(topic_id):
    sql = "select * from t_zhihu_topic_question where topic_id = %s"

    db_conn = get_conn()
    with db_conn.cursor() as cursor:
        cursor.execute(sql, topic_id)
        result = cursor.fetchall()
        db_conn.commit()
    return result


def crawl_question(topic_id):
    url = "https://www.zhihu.com/question/{0}"
    questions = get_question(topic_id)
    for question in questions:
        question_id = question['question_id']
        print(question_id)
        response = session.get(url.format(question_id), headers=headers)
        html = etree.HTML(response.text)
        answers_no = html.xpath('//h4[@class="List-headerText"]/span/text()')
        number_board = html.xpath('//div[@class="NumberBoard-value"]/text()')

        if len(answers_no) > 0:
            answers_no = answers_no[0]
        else:
            answers_no = 0
        if len(number_board) > 0:
            followers_no = number_board[0]
            views_no = number_board[1]
        else:
            followers_no = 0
            views_no = 0

        sql = 'update t_zhihu_topic_question set question_answers_no = %s, question_followers_no = %s, ' \
              'question_views_no = %s where question_id = %s'

        db_conn = get_conn()
        with db_conn.cursor() as cursor:
            cursor.execute(sql, (answers_no, followers_no, views_no, question_id))
            db_conn.commit()


if __name__ == '__main__':
    session = requests.session()
    headers = {
        "Host": "www.zhihu.com",
        "Referer": "https://www.zhihu.com/",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/63.0.3239.84 Safari/537.36"
    }
    crawl_question(20011035)
