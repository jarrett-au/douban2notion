# Python抓取豆瓣影音信息导入Notion

Created: February 4, 2022 11:47 PM
Tags: Book, Notion, Python

# 脚本下载及运行环境

---

## 脚本下载

[book2notion.py](Python%E6%8A%93%E5%8F%96%E8%B1%86%E7%93%A3%E5%BD%B1%E9%9F%B3%E4%BF%A1%E6%81%AF%E5%AF%BC%E5%85%A5Notion%203a82e824ca204cb38de08f31292d46e0/book2notion.py)

[movie2notion.py](Python%E6%8A%93%E5%8F%96%E8%B1%86%E7%93%A3%E5%BD%B1%E9%9F%B3%E4%BF%A1%E6%81%AF%E5%AF%BC%E5%85%A5Notion%203a82e824ca204cb38de08f31292d46e0/movie2notion.py)

## 系统环境

- Python3运行环境
- 请确保 Python 安装了 `lxml` 、`requests` 、`re` 、`beautifulsoup4`模块（脚本需要使用）

# 使用步骤

## 一、创建Notion API

1. 创建一个Notion机器人，
    
    [Notion - The all-in-one workspace for your notes, tasks, wikis, and databases.](https://www.notion.so/my-integrations)
    
2. 获取 `Token` 值，并复制记录，如：
    
    ![Untitled](Python%E6%8A%93%E5%8F%96%E8%B1%86%E7%93%A3%E5%BD%B1%E9%9F%B3%E4%BF%A1%E6%81%AF%E5%AF%BC%E5%85%A5Notion%203a82e824ca204cb38de08f31292d46e0/Untitled.png)
    

## 二、Duplicate 模板

1. 按需Duplicate以下模板：
    - [📚书库模板](https://www.notion.so/6a4c56ded2cc4d1a9793a0434188994d)
    - [📺追剧模板](https://www.notion.so/eb3ba38856844aa6a58954896d298c9f)
    - [🎬电影模板](https://www.notion.so/3fb8fbaea4574c73959f55f6745b9565)
2. 在模板页面点击 **Share** 按钮将刚创建的机器人 `Invite` 进去：
    
    ![Untitled](Python%E6%8A%93%E5%8F%96%E8%B1%86%E7%93%A3%E5%BD%B1%E9%9F%B3%E4%BF%A1%E6%81%AF%E5%AF%BC%E5%85%A5Notion%203a82e824ca204cb38de08f31292d46e0/Untitled%201.png)
    
3. 获取模板的 `database_id` ，并复制记录：
    
    ![Untitled](Python%E6%8A%93%E5%8F%96%E8%B1%86%E7%93%A3%E5%BD%B1%E9%9F%B3%E4%BF%A1%E6%81%AF%E5%AF%BC%E5%85%A5Notion%203a82e824ca204cb38de08f31292d46e0/Untitled%202.png)
    

## 三、运行脚本

1. 修改脚本中 `notion_api_token` 和 `notion_database_id` 变量的值
    
    ![Untitled](Python%E6%8A%93%E5%8F%96%E8%B1%86%E7%93%A3%E5%BD%B1%E9%9F%B3%E4%BF%A1%E6%81%AF%E5%AF%BC%E5%85%A5Notion%203a82e824ca204cb38de08f31292d46e0/Untitled%203.png)
    
2. 修改`subject_id`
    
    ![Untitled](Python%E6%8A%93%E5%8F%96%E8%B1%86%E7%93%A3%E5%BD%B1%E9%9F%B3%E4%BF%A1%E6%81%AF%E5%AF%BC%E5%85%A5Notion%203a82e824ca204cb38de08f31292d46e0/Untitled%204.png)
    
    ![Untitled](Python%E6%8A%93%E5%8F%96%E8%B1%86%E7%93%A3%E5%BD%B1%E9%9F%B3%E4%BF%A1%E6%81%AF%E5%AF%BC%E5%85%A5Notion%203a82e824ca204cb38de08f31292d46e0/Untitled%205.png)
    
3. 检查
    
    [屏幕录制2022-02-09 上午10.51.10.mov](Python%E6%8A%93%E5%8F%96%E8%B1%86%E7%93%A3%E5%BD%B1%E9%9F%B3%E4%BF%A1%E6%81%AF%E5%AF%BC%E5%85%A5Notion%203a82e824ca204cb38de08f31292d46e0/%E5%B1%8F%E5%B9%95%E5%BD%95%E5%88%B62022-02-09_%E4%B8%8A%E5%8D%8810.51.10.mov)