from bs4 import BeautifulSoup
import requests

# ！！！ 需要填入的两个变量值
notion_api_token = 'secret_sSzuaFEIjthAlAIK93IoVDkzFuBwk31ifUQ8I15DJaU'
# 剧集
notion_database_id = 'c0c9c1baace84e1fb4e79f307022f71c'
# 电影
# notion_database_id = '2f3716cf38994d0182116cceee00330a'


def getResqutes(url):
    # 设置请求头信息
    headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')

    # 提取电影名称，封面，评分
    mainpic = soup.find('div', id='mainpic')
    movie_name = mainpic.img['alt']
    movie_img = mainpic.img['src']
    movie_score = soup.find('div', id='interest_sectl').find('strong').text
    movie_score = float(movie_score)

    # 提取标签, 国家
    info = soup.find('div', id='info').get_text().strip().split('\n')
    info = [i.split(': ') for i in info]

    movie_tag = info[3][1]
    if len(info) == 11:
        movie_country = info[4][1]
    else:
        movie_country = info[5][1]

    if '/' in movie_tag:
        movie_tag = ', '.join(movie_tag.split(' / '))
    if '/' in movie_country:
        movie_country = movie_country.split(' / ')[0]

    body = {
        "parent": {
            "type": "database_id",
            "database_id": notion_database_id
        },
        "properties": {
            "影片名": {
                "title": [{
                    "type": "text",
                    "text": {
                        "content": movie_name
                    }
                }]
            },
            "影片链接": {
                "url": url
            },
            "封面": {
                "files": [{
                    "type": "external",
                    "name": movie_img[-13:],
                    "external": {
                        "url": movie_img
                    }
                }]
            },
            "豆瓣评分": {
                "number": movie_score
            },
            "状态": {
                "select": {
                    "name": "想看"
                }
            },
            "影片类型": {
                "rich_text": [{
                    "type": "text",
                    "text": {
                        "content": movie_tag
                    }
                }]
            },
            "国家": {
                "select": {
                    "name": movie_country
                }
            },
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
        print("导入信息成功，影片信息为：")
        print(movie_name,
              movie_score,
              movie_tag,
              movie_country,
              url,
              sep=" | ")
        print(
            '-----------------------------------------------------------------------------------------------------------------'
        )
    else:
        print("导入失败，请检查Body字段与Notion影视库字段：")
        print(NotionData.text)


if __name__ == '__main__':
    status = True
    # !!! 需要填入对应id
    subject_id = "35332289"

    while (status):
        status = False
        if (subject_id == ""):
            subject_id = input("请输入/粘贴id：")

        url = "https://movie.douban.com/subject/" + subject_id
        getResqutes(url)
