# Python抓取豆瓣影音信息导入Notion

Created: February 4, 2022 11:47 PM
Tags: Book, Notion, Python

# 脚本下载及运行环境

## 脚本下载

[book2notion.py](https://github.com/jarrett-au/douban2noition/blob/main/book2notion.py)

[movie2notion.py](https://github.com/jarrett-au/douban2noition/blob/main/movie2notion.py)

## 系统环境

- Python3运行环境
- 请确保 Python 安装了 `lxml` 、`requests` 、`re` 、`beautifulsoup4`模块（脚本需要使用）

# 使用步骤

## 一、创建Notion API

1. 创建一个Notion机器人，
    
    [Notion - The all-in-one workspace for your notes, tasks, wikis, and databases.](https://www.notion.so/my-integrations)
    
2. 获取 `Token` 值，并复制记录，如：
    
    ![token](https://raw.githubusercontent.com/jarrett-au/img_bed/master/2022/02/10_Untitled.png)
    

## 二、Duplicate 模板

1. 按需Duplicate以下模板：
    - [📚书库模板](https://www.notion.so/6a4c56ded2cc4d1a9793a0434188994d)
    - [📺追剧模板](https://www.notion.so/eb3ba38856844aa6a58954896d298c9f)
    - [🎬电影模板](https://www.notion.so/3fb8fbaea4574c73959f55f6745b9565)
2. 在模板页面点击 **Share** 按钮将刚创建的机器人 `Invite` 进去：
    
    ![Untitled](https://raw.githubusercontent.com/jarrett-au/img_bed/master/2022/02/10_Untitled%201.png)
    
3. 获取模板的 `database_id` ，并复制记录：
    
    ![Untitled](https://raw.githubusercontent.com/jarrett-au/img_bed/master/2022/02/10_Untitled%202.png)
    

## 三、运行脚本

1. 修改脚本中 `notion_api_token` 和 `notion_database_id` 变量的值
    
    ![Untitled](https://raw.githubusercontent.com/jarrett-au/img_bed/master/2022/02/10_Untitled%203.png)
    
2. 修改`subject_id`
    
    ![Untitled](https://raw.githubusercontent.com/jarrett-au/img_bed/master/2022/02/10_Untitled%204.png)
    
    ![Untitled](https://raw.githubusercontent.com/jarrett-au/img_bed/master/2022/02/10_Untitled%205.png)
    
3. 检查
    
    ![屏幕录制](https://github.com/jarrett-au/img_bed/blob/master/2022/02/10_%E5%B1%8F%E5%B9%95%E5%BD%95%E5%88%B62022-02-09_%E4%B8%8A%E5%8D%8810.51.10.2022-02-10%2021_31_31.gif?raw=true)
