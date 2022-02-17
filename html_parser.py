from bs4 import BeautifulSoup
import requests


class Parser:
    def __init__(self, url, notion_database_id):
        self.url = url
        self.notion_database_id = notion_database_id

    def get_html(self):
        headers = {
            'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
        }
        response = requests.get(self.url, headers=headers)
        return response.text

    def book_parser(self):
        soup = BeautifulSoup(self.get_html(), 'lxml')
        # 提取书名，封面，评分
        mainpic = soup.find('div', id='mainpic')
        book_name = mainpic.img['alt']
        book_img = mainpic.img['src']
        book_score = soup.find('div', id='interest_sectl').find('strong').text
        book_score = float(book_score)

        # 作者
        author_name = soup.find('div', id='info').find('a').text
        if '\n' in author_name:
            author_name = author_name.split('\n')[-1].strip()

        # 标签
        tag_list = soup.find('div', id='db-tags-section').find_all('a')
        book_tags = [tag.text for tag in tag_list]

        body = {
            "parent": {
                "type": "database_id",
                "database_id": self.notion_database_id
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
                "书籍分类": {
                    "multi_select": []
                },
                "豆瓣评分": {
                    "number": book_score
                },
                "豆瓣链接": {
                    "url": self.url
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
                "状态": {
                    "select": {
                        "name": "想读"
                    }
                },
                "作者": {
                    "rich_text": [{
                        "type": "text",
                        "text": {
                            "content": author_name
                        }
                    }]
                }
            }
        }
        # 标签处理
        for tag in book_tags[:3]:
            if tag not in [author_name, book_name]:
                body['properties']['书籍分类']['multi_select'].append(
                    {"name": tag})
        return body

    def movie_parser(self):
        soup = BeautifulSoup(self.get_html(), 'lxml')
        # 提取电影名称，封面，评分
        mainpic = soup.find('div', id='mainpic')
        movie_name = mainpic.img['alt']
        movie_img = mainpic.img['src']
        movie_score = soup.find('div', id='interest_sectl').find('strong').text
        movie_score = float(movie_score)

        # 提取标签, 国家
        info = soup.find('div', id='info').get_text().strip().split('\n')
        info = [i.split(': ') for i in info]

        # 若存在官网则国家取下一个元素
        if info[4][0] == '官方网站':
            movie_country = info[5][1]
        else:
            movie_country = info[4][1]
        # 多国家处理
        if '/' in movie_country:
            movie_country = movie_country.split(' / ')[0]

        # 提取标签
        movie_tag = info[3][1]

        body = {
            "parent": {
                "type": "database_id",
                "database_id": self.notion_database_id
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
                "影片类型": {
                    "multi_select": []
                },
                "豆瓣评分": {
                    "number": movie_score
                },
                "影片链接": {
                    "url": self.url
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
                "状态": {
                    "select": {
                        "name": "想看"
                    }
                },
                "国家": {
                    "select": {
                        "name": movie_country,
                        "color": "purple"
                    }
                },
            }
        }
        # 标签处理
        if '/' in movie_tag:
            movie_tags = movie_tag.split(' / ')
            for tag in movie_tags:
                body['properties']['影片类型']['multi_select'].append(
                    {"name": tag})
        else:
            body['properties']['影片类型']['multi_select'].append(
                {"name": movie_tag})
        return body
