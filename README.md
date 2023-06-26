利用 python 通过 Notion API 将豆瓣图书及影视信息导入 Notion，包括：书籍、电视剧及电影。

## Dependences

- `beautifulsoup4`
- `requests`
- `gooey`
- `pyinstaller`(Optional)

## Quickstart

### 创建 Notion API

1. 点击以下链接创建 Notion API，注意确保勾选了可编辑权限
    
    [Notion - The all-in-one workspace for your notes, tasks, wikis, and databases.](https://www.notion.so/my-integrations)
    
2. 获取 `Token` 值，并复制记录，如：
    
    ![notion_token](https://raw.githubusercontent.com/jarrett-au/img_bed/master/2022/02/10_Untitled.png)
    

### Duplicate 模板

<aside>
⚠️ 注意：模板数据库中的属性与python文件中的body属性为一一对应关系，如需编辑得一并修改。

</aside>

1. 按需Duplicate以下模板：
    - [📚书库模板](https://www.notion.so/6a4c56ded2cc4d1a9793a0434188994d?pvs=21)
    - [📺追剧模板](https://www.notion.so/eb3ba38856844aa6a58954896d298c9f?pvs=21)
    - [🎬电影模板](https://www.notion.so/3fb8fbaea4574c73959f55f6745b9565?pvs=21)
2. 在模板页面点击 **Share** 按钮将刚创建的机器人 `Invite` 进去：
    
    ![invite_bot](https://raw.githubusercontent.com/jarrett-au/img_bed/master/2022/02/10_Untitled%201.png)
    
3. 获取模板的 `database_id` ，并复制记录，如：
    
    ![database_id](https://raw.githubusercontent.com/jarrett-au/img_bed/master/2022/02/10_Untitled%202.png)
    

### 运行脚本

1. 安装所需依赖

```bash
pip install -r requirements.txt
```

1. 运行主程序，如果是第一次运行会提示输入 `NOTION_API_TOKEN`、`BOOK_DATABASE_ID`、`MOVIE_DATABASE_ID` 和 `TV_DATABASE_ID`，生成的配置文件 `config.json` 默认保存到相同目录下
2. 选择运行模式，并输入 `subject_id`（可输入多个，注意用英文逗号 `,` 隔开）
    
    ```bash
    python douban2notion.py
    ```
    
    ![subject_id](https://raw.githubusercontent.com/jarrett-au/img_bed/master/2022/02/10_Untitled%204.png)
    
3. （可选）下载可执行程序，或者自行 `pyinstaller` 打包
    
    ```bash
    pip install pyinstaller
    pyinstaller -Fw douban2notion.py
    ```
