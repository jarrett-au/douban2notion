from html_parser import Parser
import requests
import argparse

# 需自行修改数据库id及api_token
NOTION_API_TOKEN = ""
BOOK_DATABASE_ID = ""
MOVIE_DATABASE_ID = ""
TV_DATABASE_ID = ""

# 命令行参数
arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('-m',
                        '--mode',
                        default='book',
                        help='输入模式，book/movie/tv')
arg_parser.add_argument('-s', '--sid', help='输入subject_id')


def update_notion_database(url, mode):
    """
    更新notion数据库
    """
    if mode == 'book':
        body = Parser(url, BOOK_DATABASE_ID).book_parser()
    elif mode == 'movie':
        body = Parser(url, MOVIE_DATABASE_ID).movie_parser()
    else:
        body = Parser(url, TV_DATABASE_ID).movie_parser()

    NotionData = requests.request(
        "POST",
        "https://api.notion.com/v1/pages",
        json=body,
        headers={
            "Authorization": "Bearer " + NOTION_API_TOKEN,
            "Notion-Version": "2021-08-16"
        },
    )

    # 根据POST返回打印信息
    if (str(NotionData.status_code) == "200"):
        properties = list(body['properties'].values())
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
        print("导入失败，请检查Body字段与Notion数据库字段：")
        print(NotionData.text)


if __name__ == '__main__':
    args = arg_parser.parse_args()
    mode = args.mode
    # 参数检查
    if mode not in ['book', 'movie', 'tv']:
        raise KeyError('mode must be one of {book, movie, tv}')
    if mode == 'tv':
        opt = 'movie'
    else:
        opt = mode
    subject_id = args.sid
    url = f'https://www.douban.com/{opt}/subject/{subject_id}/'
    update_notion_database(url, mode)
