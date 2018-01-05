import json
import pymysql


def get_conn():
    db_conn = pymysql.connect(
        host="192.168.1.113",
        db="cqmall",
        user="teaman",
        passwd="qsd-a123",
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor
    )
    return db_conn


def read_log():
    f = open('/Users/wenlong/Desktop/test.log', 'r')
    try:
        sql = "insert into cq_access_log(http_referer, userId, mallUserId, openid, plat, os, action, " \
              "target_position, target_type, target, add_time) values "
        while True:
            line = f.readline()
            if line:
                obj = json.loads(line)

                if obj['msg']['logData']['userId'] is None:
                    obj['msg']['logData']['userId'] = 0
                if obj['msg']['logData']['mallUserId'] is None:
                    obj['msg']['logData']['mallUserId'] = 0
                sql += "('"+str(obj['msg']['logData']['HTTP_REFERER'])+"',"+str(obj['msg']['logData']['userId'])+","+str(obj['msg']['logData']['mallUserId']) + ",'" + str(obj['msg']['logData']['openid'])+"',"+"'"+str(obj['msg']['logData']['plat'])+"','"+str(obj['msg']['logData']['os'])+"','"+str(obj['msg']['logData']['action'])+"','"+str(obj['msg']['logData']['target_position'])+"','"+str(obj['msg']['logData']['target_type'])+"','"+str(obj['msg']['logData']['target'])+"','" + str(obj['timestamp']) + "'),"
                print(sql)
                sql = ''
            else:
                break
    finally:
        f.close()


if __name__ == '__main__':
    read_log()