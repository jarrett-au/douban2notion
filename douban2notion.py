from parser import Parser
import requests
import sys

# 需自行修改数据库id及api_token
NOTION_API_TOKEN = "secret_sSzuaFEIjthAlAIK93IoVDkzFuBwk31ifUQ8I15DJaU"
BOOK_DATABASE_ID = "a73772cc3b45446bb4fc03a2e9265af0"
MOVIE_DATABASE_ID = "2f3716cf38994d0182116cceee00330a"
TV_DATABASE_ID = "c0c9c1baace84e1fb4e79f307022f71c"


def update_notion_database(url, mode):
    if mode == 'book':
        body = Parser(url, BOOK_DATABASE_ID).book_parser()
    elif mode == 'movie':
        body = Parser(url, MOVIE_DATABASE_ID).movie_parser()
    else:
        body = Parser(url, TV_DATABASE_ID).movie_parser()

    NotionData = requests.request(
        "POST",
        # API 链接
        "https://api.notion.com/v1/pages",
        # 读取消息体，消息体需要另行编辑，后文再说
        json=body,
        # 消息头，内有必要信息
        headers={
            # 设置机器人令牌，即 Notion 的机器人码
            "Authorization": "Bearer " + NOTION_API_TOKEN,
            # 设置 Notion 版本，目前不用改
            "Notion-Version": "2021-08-16"
        },
    )

    # 根据POST返回结构打印信息
    if (str(NotionData.status_code) == "200"):
        properties = list(body['properties'].values())
        print(properties)
        name = properties[0]['title'][0]['text']['content'],
        tags = ', '.join(
            [tag['name'] for tag in properties[1]['multi_select']]),
        score = properties[2]['number'],
        print("导入信息成功，影片信息为：")
        print(name, tags, score, url, sep=" | ")
        print(
            '-----------------------------------------------------------------------------------------------------------------'
        )
    else:
        print("导入失败，请检查Body字段与Notion影视库字段：")
        print(NotionData.text)


if __name__ == '__main__':
    mode = sys.argv[1]
    if mode not in ['book', 'movie', 'tv']:
        raise ValueError('mode must be one of {book, movie, tv}')
    if mode == 'tv':
        opt = 'movie'
    else:
        opt = mode
    subject_id = sys.argv[2]
    url = f'https://www.douban.com/{opt}/subject/{subject_id}/'
    update_notion_database(url, mode)
