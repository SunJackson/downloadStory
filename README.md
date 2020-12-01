# 全网小说下载助手

## 功能

### 实现以下功能：
1. 自动根据关键词检索搜索引擎
2. 自动解析多数据源小说目录
3. 自动获取小说内容并下载
4. 实现多线程下载
5. 实现百度和SO搜索引擎的检索
6. 添加基础界面
7. 实现全局小说解析自定义配置（配置./files/config.json）

### 未来实现功能
1. 增加多个搜索引擎检索
2. 检索结果智能剔除非章节目录链接
3. 章节目录解析添加url自动识别，剔除掉非章节链接
4. 做成类似you-get

## 使用说明

1. 直接下载源码使用
- 下载源码

`git clone https://github.com/SunJackson/downloadStory.git`
- 安装依赖环境（Python3）

`pip install -r requirements.txt -i https://pypi.douban.com/simple`
- 运行代码

`python story-dl.py`（有UI界面）

或者

`pyhton src/downloadStoryMain.py`（无UI界面）

2. Windows 直接下载 exe 使用

    [小说下载工具.exe](https://github.com/SunJackson/downloadStory/releases/tag/0.1.0)

### config.json配置说明

```json
{
  "BLACK_DOMAIN": [
    ""
  ],
  "REPLACE_RULES": {
    "www.263zw.com": {
      "old": "263zw.com/402770/",
      "new": "263zw.com/402770/list/"
    }
  },
  "ENGINE_PRIORITY": [
    "so",
    "baidu"
  ],
  "REPLACE_HTML_STRING": [
    "&nbsp;"
  ],
  "CHAPTER_TAG": [
    "a"
  ],
  "CONTENT_REPLACE": {
    "\u3000\u3000": "\n",
    "\u3000": "\n",
    "加入书签": "",
    "上一章": "",
    "←": "",
    "→": "",
    "章节列表": "",
    "下一章": "",
    "顶点小说": ""
  },
  "RULES": {
	"www.vipxs.la": [
      "http://www.siluke.tw/",
      {
        "class": "box_con"
      },
      {
        "id": "content"
      }
    ]
  }
}
```