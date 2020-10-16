function getSearchResultOnclick() {
    var novel_name = document.getElementById('novel_name').value;
    var search_option = document.getElementById('search-option');
    var index = search_option.selectedIndex;
    var search_option_value = search_option.options[index].value;
    console.log(search_option_value);
    console.log(novel_name);
    if (novel_name) {
        var search_data = {
            "novel_name": novel_name,
            "search_option_value": search_option_value
        };
        console.log(search_data);
        if (search_option_value === 'bing') {
            var params={'q': novel_name}
            axios.get("https://cn.bing.com/search", {
                params: params,
                headers: {'Access-Control-Allow-Origin': '*'}//设置header信息
            }).then(resp => {
                var $ = cheerio.load(resp.data);
                console.log($);
                var lis = $("#b_results li");
                var repos = [];
                for (var i = 0; i < lis.length; i++) {
                    var li = lis.eq(i);
                    repos.push(li);
                }
                console.log(repos);
            });
        } else {
            $.ajax({
                url: 's',
                type: 'POST',     // 请求类型，常用的有 GET 和 POST
                async: true,
                data: search_data,
                success: function (data) { // 接口调用成功回调函数
                    // data 为服务器返回的数据
                    console.log(data);
                    var res_count = data.count;
                    var html_res = data.html_res;
                    var time = data.time;

                    document.getElementById("about-section").style.display = "";
                    document.getElementById("search-title").innerHTML = "<h5 class=\"wow fadeInUp\">关键词 【" + novel_name + "】 查询用时 " + time + "秒。 共查询到 " + res_count + "条数据！</h5";
                    document.getElementById("card-item").innerHTML = html_res;

                }
            });
        }
    } else {
        alert("请输入要搜索的小说名称！")
    }
}