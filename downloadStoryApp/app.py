# -*- coding: utf-8 -*-

from flask import render_template
from flask import request
from flask import Flask
from flask_bootstrap import Bootstrap

app = Flask(import_name=__name__,
            static_url_path='',  # 配置静态文件的访问 url 前缀
            static_folder='static/',  # 配置静态文件的文件夹
            template_folder='templates')  # 配置模板文件的文件夹

Bootstrap(app)  # 把程序实例即 app 传入构造方法进行初始化


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/s', methods=['POST'])
def search_novel():
    from DownloadsNovels import get_search
    print(request.form)
    novel_name = request.form['novel_name']
    search_option_value = request.form['search_option_value']
    res = get_search(novel_name, search_option_value)

    html_str_temp = """
<div class="card-body">
  <h4 class="card-title" {style}>{title}</h4>
  <p class="card-text">自动获取最新章节：{latest_chapter_name}</p>
  <p><a href="{netloc}" class="card-link">小说来源网站：{netloc}</a></p>
  <p><a href="{latest_chapter_url}" class="card-link">最新章节链接：{latest_chapter_url}</a></p>
</div>
<div class="line col-12 col-sm-12 col-md-12 col-lg-12 d-xl-flex d-lg-flex"></div>
    """
    html_res = ''
    for i in res.get('result', []):
        if not i.get('is_parse', 0):
            html_res += html_str_temp.format(title=i.get('title', ''),
                                             latest_chapter_name=i.get('latest_chapter_name', ''),
                                             netloc=i.get('netloc', ''),
                                             latest_chapter_url=i.get('url', ''),
                                             style='style="color: #9b9b9b"'
                                             )
        else:
            html_res += html_str_temp.format(title=i.get('title', ''),
                                             latest_chapter_name=i.get('latest_chapter_name', ''),
                                             netloc=i.get('netloc', ''),
                                             latest_chapter_url=i.get('url', ''),
                                             style=''
                                             )


    return {
        "count": res.get("count", 0),
        "name": res.get("name", None),
        "html_res": html_res,
        "time": res.get("time", None)
    }


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8088, debug=True)
