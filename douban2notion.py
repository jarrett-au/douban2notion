import os
import json
import requests
from bs4 import BeautifulSoup
from gooey import Gooey, GooeyParser


class Parser:
    def __init__(self, url, notion_database_id):
        self.url = url
        self.notion_database_id = notion_database_id

    def get_html(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
        }
        response = requests.get(self.url, headers=headers)
        return response.text

    def book_parser(self):
        soup = BeautifulSoup(self.get_html(), "lxml")
        # 提取书名，封面，评分
        mainpic = soup.find("div", id="mainpic")
        book_name = soup.find("meta", property="og:title")["content"]
        book_img = mainpic.img["src"]
        book_score = soup.find("div", id="interest_sectl").find("strong").text
        book_score = float(book_score)

        # 作者
        author_name = soup.find("div", id="info").find("a").text
        if "\n" in author_name:
            author_name = author_name.split("\n")[-1].strip()

        # 标签
        is_tags = soup.find("div", id="db-tags-section")
        if is_tags:
            tag_list = is_tags.find_all("a")
            book_tags = [tag.text for tag in tag_list]
        else:
            book_tags = None

        body = {
            "parent": {"type": "database_id", "database_id": self.notion_database_id},
            "properties": {
                "书名": {"title": [{"type": "text", "text": {"content": book_name}}]},
                "书籍分类": {"multi_select": []},
                "豆瓣评分": {"number": book_score},
                "豆瓣链接": {"url": self.url},
                "封面": {
                    "files": [
                        {
                            "type": "external",
                            "name": book_img[-13:],
                            "external": {"url": book_img},
                        }
                    ]
                },
                "状态": {"select": {"name": "想读"}},
                "作者": {
                    "rich_text": [{"type": "text", "text": {"content": author_name}}]
                },
            },
        }
        # 标签处理
        if book_tags:
            for tag in book_tags[:3]:
                if tag not in book_name and tag not in author_name:
                    body["properties"]["书籍分类"]["multi_select"].append({"name": tag})
        return body

    def movie_parser(self):
        soup = BeautifulSoup(self.get_html(), "lxml")
        # 提取电影名称，封面，评分
        movie_img = soup.find("div", id="mainpic").img["src"]
        movie_name = soup.find("meta", property="og:title")["content"]
        movie_score = soup.find("div", id="interest_sectl").find("strong").text
        movie_score = float(movie_score) if movie_score else 0

        # 提取标签, 国家
        info = soup.find("div", id="info").get_text().strip().split("\n")
        info = [i.split(": ") for i in info]

        # 若存在官网则国家取下一个元素
        if info[4][0] == "官方网站":
            movie_country = info[5][1]
        else:
            movie_country = info[4][1]
        # 多国家处理
        if "/" in movie_country:
            movie_country = movie_country.split(" / ")[0]

        # 提取标签
        movie_tag = info[3][1]

        body = {
            "parent": {"type": "database_id", "database_id": self.notion_database_id},
            "properties": {
                "影片名": {"title": [{"type": "text", "text": {"content": movie_name}}]},
                "影片类型": {"multi_select": []},
                "豆瓣评分": {"number": movie_score},
                "影片链接": {"url": self.url},
                "封面": {
                    "files": [
                        {
                            "type": "external",
                            "name": movie_img[-13:],
                            "external": {"url": movie_img},
                        }
                    ]
                },
                "状态": {"select": {"name": "想看"}},
                "国家": {"select": {"name": movie_country, "color": "purple"}},
            },
        }
        # 标签处理
        if "/" in movie_tag:
            movie_tags = movie_tag.split(" / ")
            for tag in movie_tags:
                body["properties"]["影片类型"]["multi_select"].append({"name": tag})
        else:
            body["properties"]["影片类型"]["multi_select"].append({"name": movie_tag})
        return body


def update_notion_database(url, mode, NOTION_API_TOKEN, BOOK_DATABASE_ID, MOVIE_DATABASE_ID, TV_DATABASE_ID):
    """
    更新notion数据库
    """
    if mode == "book":
        body = Parser(url, BOOK_DATABASE_ID).book_parser()
    elif mode == "movie":
        body = Parser(url, MOVIE_DATABASE_ID).movie_parser()
    else:
        body = Parser(url, TV_DATABASE_ID).movie_parser()

    NotionData = requests.request(
        "POST",
        "https://api.notion.com/v1/pages",
        json=body,
        headers={
            "Authorization": "Bearer " + NOTION_API_TOKEN,
            "Notion-Version": "2021-08-16",
        },
    )

    # 根据POST返回打印信息
    if str(NotionData.status_code) == "200":
        properties = list(body["properties"].values())
        name = (properties[0]["title"][0]["text"]["content"],)
        tags = (", ".join([tag["name"] for tag in properties[1]["multi_select"]]),)
        score = (properties[2]["number"],)
        print("导入信息成功，影片信息为：")
        print(name, tags, score, url, sep=" | ")
        print(
            "-----------------------------------------------------------------------------------------------------------------"
        )
    else:
        print("导入失败，请检查Body字段与Notion数据库字段：")
        print(NotionData.text)


@Gooey(language="chinese", program_name="Douban2Notion")
def main():
    # 检查是否存在配置文件
    config_file = "config.json"
    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            config = json.load(f)
    else:
        config = {}

    # 命令行参数
    arg_parser = GooeyParser(description="Douban to Notion App!")
    arg_parser.add_argument(
        "Mode", default="movie", choices=["book", "movie", "tv"], help="选择导入类型"
    )
    arg_parser.add_argument("Subject_ID", help="输入subject_id，若有多个请以英文逗号分隔")
    arg_parser.add_argument(
        "--NOTION_API_TOKEN",
        default=config.get("NOTION_API_TOKEN", ""),
        help="输入NOTION_API_TOKEN",
        widget="PasswordField",
    )
    arg_parser.add_argument(
        "--BOOK_DATABASE_ID",
        default=config.get("BOOK_DATABASE_ID", ""),
        help="输入BOOK_DATABASE_ID",
    )
    arg_parser.add_argument(
        "--MOVIE_DATABASE_ID",
        default=config.get("MOVIE_DATABASE_ID", ""),
        help="输入MOVIE_DATABASE_ID",
    )
    arg_parser.add_argument(
        "--TV_DATABASE_ID",
        default=config.get("TV_DATABASE_ID", ""),
        help="输入TV_DATABASE_ID",
    )
    args = arg_parser.parse_args()

    # 读取命令行参数
    NOTION_API_TOKEN = args.NOTION_API_TOKEN or config.get("NOTION_API_TOKEN", "")
    BOOK_DATABASE_ID = args.BOOK_DATABASE_ID or config.get("BOOK_DATABASE_ID", "")
    MOVIE_DATABASE_ID = args.MOVIE_DATABASE_ID or config.get("MOVIE_DATABASE_ID", "")
    TV_DATABASE_ID = args.TV_DATABASE_ID or config.get("TV_DATABASE_ID", "")

    # 保存参数设置
    config["NOTION_API_TOKEN"] = NOTION_API_TOKEN
    config["BOOK_DATABASE_ID"] = BOOK_DATABASE_ID
    config["MOVIE_DATABASE_ID"] = MOVIE_DATABASE_ID
    config["TV_DATABASE_ID"] = TV_DATABASE_ID
    with open(config_file, "w") as f:
        json.dump(config, f)

    mode = args.Mode
    if mode == "book":
        opt = "book"
    else:
        opt = "movie"

    subject_id = args.Subject_ID
    if "," in subject_id:
        ls_id = subject_id.split(",")
        for id in ls_id:
            url = f"https://www.douban.com/{opt}/subject/{id.strip()}/"
            update_notion_database(url, mode, NOTION_API_TOKEN, BOOK_DATABASE_ID, MOVIE_DATABASE_ID, TV_DATABASE_ID)
    else:
        url = f"https://www.douban.com/{opt}/subject/{subject_id}/"
        update_notion_database(url, mode, NOTION_API_TOKEN, BOOK_DATABASE_ID, MOVIE_DATABASE_ID, TV_DATABASE_ID)


if __name__ == "__main__":
    main()
