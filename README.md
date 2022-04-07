# **接口自动化测试框架**
## 联系方式  
QQ 529548204  
邮箱 529548204@qq.com  
如果有问题请联系我 大家共同学习共同进步~
## 操作方法
1. 新建config/config.ini文件 格式如上例子
2. 执行scripts/newProject.py
3. 在生成的test_suite/datas/名称 文件夹下增加yaml测试用例 格式如上
4. 执行writeCase.py生成测试脚本 关于token 需要根据自己项目情况修改yaml文件中token关键字 如果不需要token值为false 需要token则改为需要的类型
5. 执行/setupMain.py开始测试
## 接口录制 (测试版)

1. 代理设置  
设置计算机代理  
http=127.0.0.1:4444;https=127.0.0.1:4444;ftp=127.0.0.1:4444  
<-loopback>  
2. 浏览器设置  
新建谷歌浏览器快捷方式,右键属性 目标改为下面内容
"C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" --proxy-server=4444 --ignore-certificate-errors

如有问题请联系qq529548204

## 目录结构
    |--接口自动化测试框架 # 主目录
       ├─ common 
       ├─ config
         └─ config.ini
       ├─ testsuite
         ├─ datas
           └─ 项目文件夹 名称同config中 testname一致
              └─ login.yml # 用例数据 格式参考下面YAML PARAM格式说明
         ├─ testcase
           └─ 项目文件夹 名称同config中 testname一致 # 测试用例
             └─ test_login.py
         └─recording 录制脚本文件夹放录制的接口文档
       ├─ caches # 关联用的临时缓存文件夹
       ├─ util # 常用工具 用例生成 接口录制
         ├─ tools
         └─ scripts 
       ├─ log
       ├─ report 	
       ├─ pytest.ini	   
       ├─ requirements.txt		 
       ├─ README.md          
       └─ setupMain.py	# 整体执行程序


## yaml param格式
所有case的id 务必唯一

``` yaml

login: # caseID **请务必唯一**

  name: "登录"
  token: false # 判断此接口是否使用token false 或者"cookie"或者"Authorization"等
  # token: "Authorization"
  order: 1 # 执行顺序 @pytest.mark.run(order=1)
  file: true # bool值 true为需要文件的接口
  case:
  - info: "用户名登录-成功"
    host: 'host'
    address: '/v1/apps/$url(region_id)$/' # $url(region_id)$ 正则匹配参数中的路径参数
    method: 'post'
    
    cache: # 本地缓存 使用之后不支持分布式
      - cachefrom: 'body' # response : 从结果中获取 body : 从参数中获取
        path: '$.code' # body如果是 "id=2&path=haha" 会转换成字典 然后根据path使用jsonpath取值
        name: 'code'
      - cachefrom: 'response' # response : 从结果中获取 body : 从参数中获取
        path: '$.data'
        name: 'data'
        
    relevance:
      - relCaseName: tradeAdd # 其他testcase的ID
        relCaseNum: 1 # 关联的case数组里 第几条数据
        value: $.id # 当前返回结果的jsonpath
        name: tradeId # 关联值名称
        
    # 使用关联值方法为正则匹配$relevance(tradeId)$

    headers: {
      "Content-Type": "application/json"
    }
    data:
      file: {
        files: D:\test\test.csv # 上传文件的参数名:文件路径
      }
      param: {
        "username": "finsiot","password": "$caches(pwd)$" # 读取缓存值
      }
      urlparam: {
      id: 123
      }# 路径参数 v1/api/$url(id)$/
    assert:
      jsonpath:
         # 关联验证
        - {
          "path": "$.data.expense_trend[0].peak_hour.peak_hour",
          "value": "123", 
          "asserttype": "=="
        }
        - {
          "path": "$.code",
          "value": 0,
          "asserttype": "=="
        }
        - {
          "path": "$.data.id",
          "value": 196,
          "asserttype": "=="
        }
      sqlassert:
      # 如果不需要 此字段置空即可
        - {
          "datas": [
            {
              "path": "$.data.id",
              "name": "id"
            },
            {
              "path": "$.data.username",
              "name": "username"
            },
          ],
          "sql": "select * from saas.user where username = '****'", 
           # 取数据库查询出的第一条数据进行验证 如果存在 列名 username 值为$.data.username则通过
          "db_name": "database" # 判断链接那个数据库
          }
      time: 2 # 响应时间断言
```
## config.ini

```ini
[directory]
log_dir = /logs
data_dir = /datas
page_dir = /page
report_xml_dir = /report/xml
report_html_dir = /report/html
test_suite = /test_suite
case_dir = /testcase
cache_dir = /caches
test_name = 测试项目名称: saasWeb
[host]
http_type = http
host = 
host_117 = 
[email]
;服务器
mail_host = smtp.sina.com
;发送邮箱
mail_user = 
;口令
mail_pass = 
;发送者
sender = 
;接收邮箱
receivers = 
[database]
host = 192.
port = 3306
user = root
password = 
;database = 
database = 
charset = utf8
[dingding]
webhook = 
secret = 
```
