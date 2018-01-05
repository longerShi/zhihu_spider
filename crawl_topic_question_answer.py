import requests
import json
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


def crawl_question_answer(topic_id):
    url = 'https://www.zhihu.com/api/v4/questions/{0}/answers?' \
          'include=data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,' \
          'annotation_detail,collapse_reason,is_sticky,collapsed_by,comment_count,can_comment,editable_content,' \
          'voteup_count,reshipment_settings,comment_permission,created_time,updated_time,review_info,question,' \
          'excerpt,is_author,voting,is_thanked,is_nothelp,upvoted_followees;' \
          'data[*].mark_infos[*].url;data[*].author.follower_count,badge[?(type=best_answerer)].topics' \
          '&offset={1}&limit=20&sort_by=default'

    questions = get_question(topic_id)
    for question in questions:
        question_id = question['question_id']
        crawl_question_answer(topic_id, question_id, url.format(question_id, 0))


def crawl_question_answer(topic_id, question_id, url):
    response = session.get(url, headers=headers)
    resp_json = json.loads(response.text)
    datas = resp_json['data']
    i = 0

    answer_sql = "insert into t_zhihu_topic_question_answer" \
             "(topic_id, question_id, answer_id, answer_user_name, answer_like_no, answer_comment_no) values"

    while len(datas) > 0:
        for data in datas:
            ++i
            answer_id = data['id']
            voteup_count = data['voteup_count']
            comment_count = data['comment_count']
            user_name = data['author']['name']
            url_token = data['author']['url_token']
            answer_sql += "("+str(topic_id)+","+str(question_id)+","+str(answer_id)+",'"+str(user_name)+"',"+\
                          str(voteup_count)+","+str(comment_count)+"),"
            if i == 20:
                print(i)
                i = 0
        crawl_question_answer(topic_id, question_id, datas['paging']['next'])

if __name__ == '__main__':
    session = requests.session()
    headers = {
        "Host": "www.zhihu.com",
        "Referer": "https://www.zhihu.com/",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/63.0.3239.84 Safari/537.36",
        "authorization": "Bearer Mi4xWkk4QkF3QUFBQUFBa0VJdWQ5alVEQmNBQUFCaEFsVk5hWG9mV3dEM0VwTWlmbDhBeEdOYVJPLVIybHR4cE"
                 "tXN1hB|1513237609|5e82cc785ca31de90f345ad1db5f4662b2cfd123"

    }
    crawl_question_answer(20011035)
