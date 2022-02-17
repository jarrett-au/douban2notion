# Python抓取豆瓣图书、影视导入Notion

利用 python 通过 Notion API 将豆瓣图书及影视信息导入 Notion，具体导入格式请参考下方模板的数据库样式。

![demo](https://raw.githubusercontent.com/jarrett-au/img_bed/master/2022/02/14_demo.gif)

## Dependencies
- `beautifulsoup4`
- `requests`

## Quickstart

### 创建 Notion API
1. 点击以下链接创建 Notion API，注意确保勾选了可编辑权限

    [Notion - The all-in-one workspace for your notes, tasks, wikis, and databases.](https://www.notion.so/my-integrations)

    
2. 获取 `Token` 值，并复制记录，如：
    
    ![token](https://raw.githubusercontent.com/jarrett-au/img_bed/master/2022/02/10_Untitled.png)
    

### Duplicate 模板

注意：模板数据库中的属性与python文件中的body属性为一一对应关系，如需编辑得一并修改。

1. 按需Duplicate以下模板：
    - [📚书库模板](https://www.notion.so/6a4c56ded2cc4d1a9793a0434188994d)
    - [📺追剧模板](https://www.notion.so/eb3ba38856844aa6a58954896d298c9f)
    - [🎬电影模板](https://www.notion.so/3fb8fbaea4574c73959f55f6745b9565)


2. 在模板页面点击 **Share** 按钮将刚创建的机器人 `Invite` 进去：
    
    ![share](https://raw.githubusercontent.com/jarrett-au/img_bed/master/2022/02/10_Untitled%201.png)
    
3. 获取模板的 `database_id` ，并复制记录，如：
    
    ![database_id](https://raw.githubusercontent.com/jarrett-au/img_bed/master/2022/02/10_Untitled%202.png)
    

### 运行脚本

1. 修改脚本中 `NOTION_API_TOKEN` 和所需的 `DATABASE_ID` 变量的值
    
    ![TOKEN](https://raw.githubusercontent.com/jarrett-au/img_bed/master/2022/02/14_T6LzEG.png)
    
2. 运行以下命令：
    > python douban2notion.py -m [mode] -s [subject_id]
    - `-h`: 帮助
    - `-m`: book / movie / tv
    - `-s`: subject_id

    ![subject_id](https://raw.githubusercontent.com/jarrett-au/img_bed/master/2022/02/10_Untitled%204.png)
