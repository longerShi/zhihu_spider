import requests
import pymysql
import urllib
from lxml import etree
from lxml.html.clean import Cleaner


def get_conn():
    db_conn = pymysql.connect(
        host="localhost",
        db="wechat",
        user="root",
        passwd="123456",
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor
    )
    return db_conn


def get_district(code):
    sql = "select * From t_district where code = %s"

    db_conn = get_conn()
    with db_conn.cursor() as cursor:
        cursor.execute(sql, code)
        result = cursor.fetchall()
        db_conn.commit()
    return result


def get_page_html(url):
    page = urllib.request.urlopen(url, timeout=10).read()
    cleaner = Cleaner(style=True, scripts=True, page_structure=False, safe_attrs_only=False)  # 清除掉CSS等
    texts = etree.HTML(cleaner.clean_html(page), parser=etree.HTMLParser(encoding='utf-8'))
    # texts = etree.HTML(page, parser=etree.HTMLParser(encoding='utf-8'))
    return texts


def crawl_district():
    host = 'http://www.diqudaima.com'
    url = host + '/hunan/changdeshi/index.html'
    texts = get_page_html(url)
    codeStrArr = texts.xpath("//ul/li/text()")
    hrefArr = texts.xpath("//ul/li/a/@href")

    for index, codeStr in enumerate(codeStrArr):
        id = get_district(codeStr.split("：")[1].split(" ")[0])[0]['id']

        texts1 = get_page_html(host+hrefArr[index])
        codeStrArr1 = texts1.xpath('//ul/li/a/@href')
        add = texts1.xpath('//ul/li/a/text()')
        pName = texts1.xpath('//div[@class="NameSzu"]/text()')[0]
        for index, codeStr in enumerate(codeStrArr1):
            code = codeStr.split('/')[2].split(".")[0]
            print("insert into t_district(name, parent_id, code, orderr) value('" +add[index].replace(pName, '')+"',"+str(id)+","+str(code)+","+str(index)+");")


if __name__ == '__main__':
    crawl_district()
