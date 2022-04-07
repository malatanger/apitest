# coding:utf-8
import datetime
import hashlib
import random
import re
import time
import string
import jsonpath
from faker import Faker
from util.tools.caches import Cache


def choice_data(data):
    """
    获取随机整型数据
    :param data: 数组
    :return:
    """
    _list = data.split(",")
    num = random.choice(_list)
    return num


def random_float(data):
    """
    获取随机整型数据
    :param data: 数组
    :return:
    """
    try:
        start_num, end_num, accuracy = data.split(",")
        start_num = int(start_num)
        end_num = int(end_num)
        accuracy = int(accuracy)
    except ValueError:
        raise Exception("调用随机整数失败，范围参数或精度有误！\n小数范围精度 %s" % data)

    if start_num <= end_num:
        num = random.uniform(start_num, end_num)
    else:
        num = random.uniform(end_num, start_num)
    num = round(num, accuracy)
    return num


def md5(data):
    """
    md5加密
    :param data:想要加密的字符
    :return:
    """
    m1 = hashlib.md5()
    m1.update(data.encode("utf-8"))
    data = m1.hexdigest()
    return data


def sql_json(jspath, res):
    # 根据jsonpath从结过中获取值
    return jsonpath.jsonpath(res, jspath)[0]


def nomal(paramname, param:dict):
    # 从字典中取值
    return param[paramname]

def caches(data):
    # 从缓存中获取
    c = Cache()
    return c.get(data)



def random_int(scope):
    """
    获取随机整型数据
    :param scope: 数据范围
    :return:
    """
    try:
        start_num, end_num = scope.split(",")
        start_num = int(start_num)
        end_num = int(end_num)
    except ValueError:
        raise Exception("调用随机整数失败，范围参数有误！\n %s" % str(scope))
    if start_num <= end_num:
        num = random.randint(start_num, end_num)
    else:
        num = random.randint(end_num, start_num)

    return num





def random_string(num_len):
    """
    从a-zA-Z0-9生成制定数量的随机字符
    :param num_len: 字符串长度
    :return:
    """
    try:
        num_len = int(num_len)
    except ValueError:
        raise Exception("从a-zA-Z0-9生成指定数量的随机字符失败！长度参数有误  %s" % num_len)
    strings = ''.join(random.sample(string.hexdigits, +num_len))
    return strings


def get_time(time_type, layout, unit="0,0,0,0,0"):
    """
    获取时间
    :param time_type: 现在的时间now， 其他时间else_time
    :param layout: 10timestamp，13timestamp, else  时间类型
    :param unit: 时间单位：[seconds, minutes, hours, days, weeks] 秒，分，时，天，周，所有参数都是可选的，并且默认都是0
    :return:
    python中时间日期格式化符号：
    ------------------------------------
    %y 两位数的年份表示（00-99）
    %Y 四位数的年份表示（000-9999）
    %m 月份（01-12）
    %d 月内中的一天（0-31）
    %H 24小时制小时数（0-23）
    %I 12小时制小时数（01-12）
    %M 分钟数（00=59）
    %S 秒（00-59）
    %a 本地简化星期名称
    %A 本地完整星期名称
    %b 本地简化的月份名称
    %B 本地完整的月份名称
    %c 本地相应的日期表示和时间表示
    %j 年内的一天（001-366）
    %p 本地A.M.或P.M.的等价符
    %U 一年中的星期数（00-53）星期天为星期的开始
    %w 星期（0-6），星期天为星期的开始
    %W 一年中的星期数（00-53）星期一为星期的开始
    %x 本地相应的日期表示
    %X 本地相应的时间表示
    %Z 当前时区的名称  # 乱码
    %% %号本身

    # datetime.timedelta 代表两个时间之间的时间差
    # time.strftime(fmt[,tupletime]) 接收以时间元组，并返回以可读字符串表示的当地时间，格式由fmt决定
    # time.strptime(str,fmt='%a %b %d %H:%M:%S %Y') 根据fmt的格式把一个时间字符串解析为时间元组
    # time.mktime(tupletime) 接受时间元组并返回时间戳（1970纪元后经过的浮点秒数）


    """
    ti = datetime.datetime.now()
    if time_type == "future":
        resolution = unit.split(",")
        try:
            ti = ti + datetime.timedelta(seconds=int(resolution[0]), minutes=int(resolution[1]),
                                         hours=int(resolution[2]), days=int(resolution[3]), weeks=int(resolution[4]))
        except ValueError:
            raise Exception("获取时间错误，时间单位%s" % unit)
    elif time_type == "past":
        resolution = unit.split(",")
        try:
            ti = ti - datetime.timedelta(seconds=int(resolution[0]), minutes=int(resolution[1]),
                                         hours=int(resolution[2]), days=int(resolution[3]), weeks=int(resolution[4]))
        except ValueError:
            raise Exception("获取时间错误，时间单位%s" % unit)
    if layout == "10timestampNOW":
        ti = ti.strftime('%Y-%m-%d %H:%M:%S')
        ti = int(time.mktime(time.strptime(ti, "%Y-%m-%d %H:%M:%S")))
        return ti
    elif layout == "13timestampNOW":
        ti = ti.strftime('%Y-%m-%d %H:%M:%S')
        ti = int(time.mktime(time.strptime(ti, '%Y-%m-%d %H:%M:%S')))
        # round()是四舍五入
        ti = int(round(ti * 1000))
        return ti
    elif layout == "13timestampDAY":
        ti = ti.strftime('%Y-%m-%d 00:00:00')
        ti = int(time.mktime(time.strptime(ti, '%Y-%m-%d %H:%M:%S')))
        # round()是四舍五入
        ti = int(round(ti * 1000))
        return ti
    elif layout == "10timestampDAYA":
        ti = ti.strftime('%Y-%m-%d 00:00:00')
        ti = int(time.mktime(time.strptime(ti, "%Y-%m-%d %H:%M:%S")))
        return ti
    else:
        ti = ti.strftime(layout)
        return ti

def fakerdata(data):
    """
    :param data: phone_number 手机号: "$faker(phone_number)$" idcard 身份证: "$faker(idcard)$"
    province 随机生成省  city 随机生成市
    :return:
    """
    fake = Faker("zh_CN")
    if data == "idcard":
        value = fake.ssn()
        return value
    elif data == "province":
        value = fake.province()
        return value
    elif data == "city":
        value = fake.city()
        return value
    elif data == "phone_number":
        value = fake.phone_number()
        return value
    elif data == "name":
        value = fake.name()
        return value
    elif data == "email":
        value = fake.email()
        return value


def replace_random(value, res=None, param=None):
    """
    调用定义方法替换字符串
    int_num = "$RandomPosInt(1,333)$"
    str_num = '$RandomString($RandomPosInt(2,23)$)$$RandomPosInt(1,333)$'
    float_num = '$RandomFloat($RandomPosInt(2,13)$,$RandomPosInt(2,13)$,$RandomPosInt(2,13)$)$'
    time_num = '$GetTime(time_type=else,layout=%Y-%m-%d %H:%M:%S,unit=0,0,0,0,0)$'
    choice_num = '$Choice($RandomPosInt(2,13)$)$'
    json_value = '$json($.data[-$RandomPosInt(1,5)$:])$'
    urls = "$url(home_id)$"
    ca = "$caches(haha)$"

    phonenumber = "$faker(phone_number)$" # 电话号码

    d = {"id":2}
    print(replace_random("$relevance(id)$",param=d)) # 获取关联


    print(replace_random(urls,param={"home_id":"$caches(haha)$"}))
    print(replace_random(ca))
    :param param: 路径参数数据
    :param res: jsonpath使用的返回结果
    :param value:
    :return:
    """
    posint_list = re.findall(r"\$RandomPosInt\(([0-9]*,[0-9]*?)\)\$", value)
    int_list = re.findall(r'\$RandomInt\((-[0-9]*,[0-9]*?)\)\$', value)
    string_list = re.findall(r'\$RandomString\(([0-9]*?)\)\$', value)
    float_list = re.findall(r'\$RandomFloat\(([0-9]*,[0-9]*,[0-9]*)\)\$', value)
    time_list = re.findall(r"\$GetTime\(time_type=(.*?),layout=(.*?),unit=([0-9],[0-9],[0-9],[0-9],[0-9])\)\$", value)
    choice_list = re.findall(r"\$Choice\((.*?)\)\$", value)
    sqljson_list = re.findall(r"\$json\((.*?)\)\$", value)
    urlparam_list = re.findall(r"\$url\((.*?)\)\$", value)
    caches_list = re.findall(r"\$caches\((.*?)\)\$", value)
    idcard_list = re.findall(r"\$faker\((.*?)\)\$", value)
    relevance_list = re.findall(r"\$relevance\((.*?)\)\$", value)

    if len(int_list):
        # 获取整型数据替换
        for i in int_list:
            pattern = re.compile(r'\$RandomInt\(' + i + r'\)\$')
            key = str(random_int(i))
            value = re.sub(pattern, key, value, count=1)
        value = replace_random(value, res ,param)
    elif len(posint_list):
        # 获取整型数据替换
        for i in posint_list:
            pattern = re.compile(r'\$RandomPosInt\(' + i + r'\)\$')
            key = str(random_int(i))
            value = re.sub(pattern, key, value, count=1)
        value = replace_random(value, res,param)
    elif len(string_list):
        # 获取字符串数据替换
        for i in string_list:
            pattern = re.compile(r'\$RandomString\(' + i + r'\)\$')
            key = str(random_string(i))
            value = re.sub(pattern, key, value, count=1)
        value = replace_random(value, res,param)

    elif len(float_list):
        # 获取浮点数数据替换
        for i in float_list:
            pattern = re.compile(r'\$RandomFloat\(' + i + r'\)\$')
            key = str(random_float(i))
            value = re.sub(pattern, key, value, count=1)
        value = replace_random(value, res,param)

    elif len(time_list):
        # 获取时间替换
        for i in time_list:
            if len(i[0]) and len(i[1]):
                pattern = re.compile(r'\$GetTime\(time_type=' + i[0] + ',layout=' + i[1] + ',unit=' + i[2] + r'\)\$')
                key = str(get_time(i[0], i[1], i[2]))
                value = re.sub(pattern, key, value, count=1)
            else:
                print("$GetTime$参数错误，time_type, layout为必填")
        value = replace_random(value, res,param)

    elif len(choice_list):
        # 调用choice方法
        for i in choice_list:
            pattern = re.compile(r'\$Choice\(' + i + r'\)\$')
            key = str(choice_data(i))
            value = re.sub(pattern, key, value, count=1)
        value = replace_random(value, res,param)

    elif len(sqljson_list):
        for i in sqljson_list:
            pattern = re.compile(r'\$json\(' + i.replace('$', "\$").replace('[', '\[') + r'\)\$')
            key = str(sql_json(i, res))
            value = re.sub(pattern, key, value, count=1)
        value = replace_random(value, res,param)

    elif len(urlparam_list):

        # urls = "$url(home_id)$"
        # replace_random(urls,param={"home_id":"$caches(haha)$"})
        for i in urlparam_list:
            pattern = re.compile(r'\$url\(' + i + r'\)\$')
            key = str(nomal(i, param))
            value = re.sub(pattern, key, value, count=1)
        value = replace_random(value,res, param=param)

    elif len(relevance_list):

        # urls = "$url(home_id)$"
        # replace_random(urls,param={"home_id":"$caches(haha)$"})
        for i in relevance_list:
            pattern = re.compile(r'\$relevance\(' + i + r'\)\$')
            key = str(nomal(i, param))
            value = re.sub(pattern, key, value, count=1)
        value = replace_random(value,res, param=param)

    elif len(caches_list):
        # urls = "$url(home_id)$"
        # replace_random(urls,param={"home_id":"$caches(haha)$"})
        for i in caches_list:
            pattern = re.compile(r'\$caches\(' + i + r'\)\$')
            key = str(caches(i))
            value = re.sub(pattern, key, value, count=1)
        value = replace_random(value,res,param=param)
    elif len(idcard_list):
        # 调用choice方法
        for i in idcard_list:
            pattern = re.compile(r'\$faker\(' + i + r'\)\$')
            key = str(fakerdata(i))
            value = re.sub(pattern, key, value, count=1)
        value = replace_random(value, res,param)
    else:
        pass
    return value


if __name__ == '__main__':
    int_num = "$RandomPosInt(1,333)$"
    str_num = '$RandomString($RandomPosInt(2,23)$)$$RandomPosInt(1,333)$'
    float_num = '$RandomFloat($RandomPosInt(2,13)$,$RandomPosInt(2,13)$,$RandomPosInt(2,13)$)$'
    time_num = '$GetTime(time_type=else,layout=%Y-%m-%d %H:%M:%S,unit=0,0,0,0,0)$'
    choice_num = '$Choice($RandomPosInt(2,13)$)$'
    '$json($.data[-$RandomPosInt(1,5)$:])$'
    jsons = """
select count(*) '$json($.data[-$RandomPosInt(1,5)$:])$'
$RandomString($RandomPosInt(2,23)$)$
    ) as ad
    """
    js = """
    select count(*) '$json($.data[-$RandomPosInt(1,5)$:])$' from (
select
       dr.qr_code,
       alarm.device_id,
       alarm.grade,
       alarm.create_time,
       alarm.handler_status,
       alarm.work_order

from alarm
         inner join (
    select device.id,
           device.qr_code,
           device.region_id,
           region.enterprise_id,
           device.status,
           device.category_id
    from device
             inner join region
                        on device.region_id = region.id
                            and region.enterprise_id = 88
) as dr
                    on dr.qr_code = alarm.device_id and alarm.create_time >= '$GetTime(time_type=past,layout=%Y-%m-%d 00:00:00,unit=0,0,0,1,0)$' and alarm.create_time < '$GetTime(time_type=past,layout=%Y-%m-%d 00:00:00,unit=0,0,0,0,0)$'
    ) as ad
    """
    # a = json.dumps(ini_yaml("homePageData.yml")["companyAlarm"])
    # print(type(ini_yaml("家庭详情.yml")[0]["data"]))
    print(replace_random(int_num))
    print(replace_random(str_num))
    print(replace_random(float_num))
    print(replace_random(time_num))

    res1 = {'code': 0, 'msg': 'ok',
            'data': [{'time': '2021-08-18', 'number': None}, {'time': '2021-08-19', 'number': None},
                     {'time': '2021-08-20', 'number': 1}, {'time': '2021-08-21', 'number': None},
                     {'time': '2021-08-22', 'number': None}, {'time': '2021-08-23', 'number': 9}]}
    idc = "$faker(email)$"
    print(replace_random(idc))
    t = "$GetTime(time_type=past,layout=13timestampDAY,unit=0,0,0,1,4)$"
    # print(replace_random(choice_num))
    # print(replace_random(urls,param={"home_id":"$caches(haha)$"}))
    # print(replace_random(ca))
    # pattern = re.compile(r'\$json\(' + '$.data.alarm[1].number'.replace('$',"\$").replace('[','\[') + r'\)\$')
    # # key = str(sql_json(i))
    # key = "123"
    # value = re.sub(pattern, "*", jsons, count=1)
    # print(value)
    # p = {'firmwareId': 187, 'firmwareId2': 187}
    # d = {'info': '固件详情', 'host': 'host', 'address': '/v1/device/firmware/$url(firmwareId)$/', 'method': 'get',
    #      'cache': None,
    #      'relevance': [{'relCaseName': 'firmwareList', 'relCaseNum': 1, 'value': '$.data[0].id', 'name': 'firmwareId'},
    #                    {'relCaseName': 'firmwareList', 'relCaseNum': 1, 'value': '$.data[0].id', 'name': 'firmwareId2'}],
    #      'headers': {'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': None},
    #      'data': {'param': None, 'urlparam': {'firmwareId': '$caches(firmwareId)$'}}, 'assert': {
    #         'jsonpath': [{'path': '$.msg', 'value': 'Success.', 'asserttype': '==', 'relevanceCheck': None},
    #                      {'path': '$.code', 'value': 0, 'asserttype': '==', 'relevanceCheck': None}], 'sqlassert': None,
    #         'time': 2}}
    #
    # a = replace_random(str(d),param=p)
    # print(a)
