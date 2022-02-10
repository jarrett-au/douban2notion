from lxml import etree
import requests
import re

# ！！！需要填入的两个变量值
notion_database_id = 'a73772cc3b45446bb4fc03a2e9265af0'
notion_api_token = 'secret_sSzuaFEIjthAlAIK93IoVDkzFuBwk31ifUQ8I15DJaU'


def getResqutes(url):
    # 设置请求头信息
    headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }

    data = requests.get(url, headers=headers)  # 此处是请求
    html = etree.HTML(data.text)  # 网页的解析

    # 书名
    book_name = html.xpath("//*[@id='mainpic']/a/@title")
    # 图片url
    book_img = html.xpath("//*[@id='mainpic']/a/img/@src")
    # 作者
    author_name = html.xpath("//*[@id='info']/span[1]/a/text()")
    if (author_name == ""):
        author_name = html.xpath(u'//span[text()="作者:"]/../a[1]/text()')
        author_name = re.sub(r'[(\s)*(\n)*]',
                             "",
                             author_name,
                             count=0,
                             flags=0)

    # 评分
    book_score = html.xpath(
        "//*[@id='interest_sectl']/div/div[2]/strong/text()")
    # 图书简介
    # introduction = html.xpath(u'//span[text()="内容简介"]/../following::div[1]//div[@class="intro"]/p/text()')

    # 标签
    book_tag = html.xpath("//*[@id='db-tags-section']/div/span/a//text()")

    # list转成string
    book_name = ''.join(book_name)
    author_name = ''.join(author_name).strip()
    book_img = ''.join(book_img).strip()
    book_score = ''.join(book_score).strip()
    # 评分转为Num
    book_score = float(book_score)

    body = {
        "parent": {
            "type": "database_id",
            "database_id": notion_database_id
        },
        "properties": {
            "书名": {
                "title": [{
                    "type": "text",
                    "text": {
                        "content": book_name
                    }
                }]
            },
            "作者": {
                "rich_text": [{
                    "type": "text",
                    "text": {
                        "content": author_name
                    }
                }]
            },
            "豆瓣链接": {
                "url": data.url
            },
            "封面": {
                "files": [{
                    "type": "external",
                    "name": book_img[-13:],
                    "external": {
                        "url": book_img
                    }
                }]
            },
            "豆瓣评分": {
                "number": book_score
            },
            "状态": {
                "select": {
                    "name": "想读"
                }
            },
            "书籍分类": {
                "multi_select": [{
                    "name": book_tag[0],
                }, {
                    "name": book_tag[1]
                }]
            }
        }
    }

    # 向 Notion API 发送HTTP请求
    NotionData = requests.request(
        "POST",
        # API 链接
        "https://api.notion.com/v1/pages",
        # 读取消息体，消息体需要另行编辑，后文再说
        json=body,
        # 消息头，内有必要信息
        headers={
            # 设置机器人令牌，即 Notion 的机器人码
            "Authorization": "Bearer " + notion_api_token,
            # 设置 Notion 版本，目前不用改
            "Notion-Version": "2021-08-16"
        },
    )

    # 根据POST返回结构打印信息
    if (str(NotionData.status_code) == "200"):
        print("导入信息成功，图书信息为：")
        print(book_name,
              author_name,
              book_score,
              data.url,
              ', '.join(book_tag[:2]),
              sep=" | ")
        print(
            '-----------------------------------------------------------------------------------------------------------------'
        )
    else:
        print("导入失败，请检查Body字段与Notion书库字段：")
        print(NotionData.text)


if __name__ == '__main__':
    status = True
    # !!! 需要填入对应id
    subject_id = "35720052"

    while (status):
        status = False
        if (subject_id == ""):
            subject_id = input("请输入/粘贴id：")

        url = "https://book.douban.com/subject/" + subject_id
        getResqutes(url)
