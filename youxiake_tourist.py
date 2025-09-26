import requests
import pandas as pd
from bs4 import BeautifulSoup
import time

base_url = "https://www.youxiake.com/mytravel"

headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Connection': 'keep-alive',
        'Cookie': 'pingtaiw=0; yxk_auth=30f0bfHaklud1x0ycEYoQOlu2coLkx1BM3gIp4bjHBlL4c9gFLfKVu3qYFC17ZgQX91NwAjy%2BQ2U9qCYZjSms7dtX3mPjg; access_token=Bearer%20eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvd3d3LnlvdXhpYWtlLmNvbVwvbG9naW5cL3ZlcmlmeSIsImlhdCI6MTczMDk3NzExMywiZXhwIjoxNzMwOTgwNzEzLCJuYmYiOjE3MzA5NzcxMTMsImp0aSI6IjUyM2FnaVRITVBmUURxMnAiLCJzdWIiOjEwNTk4MDgxLCJwcnYiOiIwYmMzYTRmYmEzYTExOTllY2MwNjU3ODg4MGEzZWJhZTQwZTJlOWFjIn0.0BMT3YHiVazbsBw9jlK9s0IXdTMBWKsn97yPwNeIzXY; sitecode=1; site=1; gr_user_id=b3782b24-f4d6-479b-911a-a575b18aeed5; a147ace5a8874284_gr_session_id=39672af5-5914-4b87-b50e-9894ef07d516; a147ace5a8874284_gr_last_sent_sid_with_cs1=39672af5-5914-4b87-b50e-9894ef07d516; a147ace5a8874284_gr_last_sent_cs1=10598081; _ga=GA1.2.908587001.1732030045; _gid=GA1.2.1785569538.1732030045; a147ace5a8874284_gr_session_id_sent_vst=39672af5-5914-4b87-b50e-9894ef07d516; sideMuenShop=1; Hm_lvt_4668967a6a0541a2a7cb9bf90df08bdd=1730976938,1732030046; HMACCOUNT=4C9682343569D7D4; PHPSESSID=4161b011b073c6e452d3cfd0b30f4 	a17; _gat=1; a147ace5a8874284_gr_cs1=10598081; yxk_session=eyJpdiI6InB3Zk9PdEQ0clZQUHFYeDlIeGNSN3c9PSIsInZhbHVlIjoiUGNiaFNhZlZUcG5Yc2JKakxYbjh1dWJhSyszd3RmbkxrajNWdHVXWHFoT3ZxdU1vMURaRWdRbVJId0x1dXRzUVFmTVNIMXJCekZXNVVSY09NU0h4WkJ1QUVQTnVuK081bWk2Smp1SlhYWHlUNHhCRUpKaWE3d0h1OVBhK0RPMmIiLCJtYWMiOiIyNDJjMDNiMDQ3OWRmNWM0YmU3NWJmMDhmMjYwMTNjMWE0Y2Y1MDA4NGNiMzMxNjJiZmQxZDJkODA3YzdhYzViIn0%3D; yxk_last_visit=1732030566; Hm_lpvt_4668967a6a0541a2a7cb9bf90df08bdd=1732030567',
        # 注意：这里只展示了部分Cookie，你需要使用完整的Cookie字符串
        'Host': f'www.youxiake.com',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0',
        'Sec-Ch-Ua': '"Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"'
    }

def query_all_user_info():
    '''<a href="https://www.youxiake.com/mytravel/edittourist?id=1471289"'''

    user_list = []

    def get_user_id(res_txt):
        id_list = []
        for line in res_txt.split('\n'):
            if "https://www.youxiake.com/mytravel/edittourist?id=" in line:
                user_id = line.split("id=")[1]
                # print(user_id[0:-1])
                id_list.append(user_id[0:-1])
        return id_list

    def get_user_info(res_txt):
        user_info_list = []
        # 使用BeautifulSoup解析HTML
        soup = BeautifulSoup(res_txt, 'html.parser')

        # 找到具有class="m-table"的table元素
        table = soup.find('table', class_='m-table')

        # 遍历table下的所有tr元素（除了表头）
        for row in table.find_all('tr')[1:]:  # [1:] 跳过了表头行

            user_info = {}

            # 提取每一行的td元素
            cols = row.find_all('td')

            # 提取用户名（第一个td元素）
            user_info["username"] = cols[0].get_text(strip=True)

            # 提取性别（第二个td元素）
            user_info["sex"] = cols[1].get_text(strip=True)

            # 提取类型（第三个td元素）
            user_info["m_type"] = cols[2].get_text(strip=True)

            # 提取身份证号（第五个td元素）
            user_info["id_number"] = cols[4].get_text(strip=True)

            # 提取手机号（第六个td元素）
            user_info["phone_number"] = cols[5].get_text(strip=True)

            # 提取id（第九个td元素）
            id_url = str(cols[8].find_all('a')[0])
            user_info["m_id"] = id_url.split("id=")[1].split('"')[0]

            # 打印或存储这些信息
            #print(user_info)
            user_info_list.append(user_info)
        return user_info_list

    # 目标URL
    url = f'{base_url}/tourist'

    # 构建请求标头


    # 发送GET请求
    try:
        response = requests.get(url, headers=headers)

        # 检查请求是否成功
        if response.status_code == 200:
            # 获取并打印返回的内容
            print("请求成功!")
            #print(response.text)
            #user_id_list = get_user_id(response.text)
            user_list = get_user_info(response.text)
        else:
            print(f"请求失败，状态码：{response.status_code}")

    except requests.RequestException as e:
        # 处理请求异常
        print(f"请求过程中发生异常：{e}")
    finally:
        return user_list

def del_tourist(user_id):
    url = f"https://www.youxiake.com/mytravel/deltourist?id={user_id}"
    # 发送GET请求
    try:
        response = requests.get(url, headers=headers)

        # 检查请求是否成功
        if response.status_code == 200:
            # 获取并打印返回的内容
            print(f"{user_id} 删除成功!")
        else:
            print(f"请求失败，状态码：{response.status_code}")

    except requests.RequestException as e:
        # 处理请求异常
        print(f"请求过程中发生异常：{e}")

def read_user_info_from_xlsx(file_path):
    # 读取Excel文件
    df = pd.read_excel(file_path, header=1)
    #print(df)

    # 创建新列名映射
    column_mapping = {}
    # 重命名列名以匹配代码中的引用（如果列名与示例不完全匹配）
    for col in df.columns:
        if '姓名' in col:
            column_mapping[col] = '姓名'
        if '手机号' in col:
            column_mapping[col] = '手机号'
        if '身份证' in col:
            column_mapping[col] = '身份证号'
        if '性别' in col:
            column_mapping[col] = '性别'
        if '类型' in col:
            column_mapping[col] = '类型'

    df.rename(columns=column_mapping, inplace=True)

    # 添加一个“类型”列，如果原表中没有则默认为“成人”
    if '类型' not in df.columns:
        df['类型'] = '成人'

    # 选择需要的列
    required_columns = ['姓名', '手机号', '身份证号', '性别', '类型']
    df_selected = df[required_columns]

    # 显示结果
    #print(df_selected)
    records = [
        {
            '姓名': row['姓名'],
            '手机号': row['手机号'],
            '身份证号': row['身份证号'],
            '性别': row['性别'],
            '类型': row['类型'],  # 直接设置默认值
        }
        for index, row in df.iterrows()
    ]

    user_info_records = []

    # 打印结果
    for record in records:
        print(record)
        user_info = {
            'realname': record['姓名'],
            'cardtype': '1',
            'cardno': record['身份证号'],
            'cardexp': '',
            'cardexp_hk': '',
            'typepassport': '1',
            'passport_china': '1',
            'passport_out': '3575',
            'birthday': '',
            'phone': str(record['手机号']),
            'type': '',
            'sex': '',
            'mid': ''
        }
        if record['性别'] == '男':
            user_info['sex'] = '1'
        if record['性别'] == '女':
            user_info['sex'] = '2'
        if record['类型'] == '成人':
            user_info['type'] = '1'
        if record['类型'] == '儿童':
            user_info['type'] = '2'
        print(user_info)
        user_info_records.append(user_info)

    return user_info_records

def add_user(user_info):

    def check_error(res_txt):
        for each in res_txt.split('\n'):
            if "添加常用游客成功" in each:
                return True
        return False

    url = f'{base_url}/tourist'
    # 准备表单数据
    data = {
        'realname': '吴斯航',
        'cardtype': '1',
        'cardno': '372901200008028313',
        'cardexp': '',
        'cardexp_hk': '',
        'typepassport': '1',
        'passport_china': '1',
        'passport_out': '3575',
        'birthday': '',
        'phone': '19863736775',
        'type': '2',
        'sex': '2',
        'mid': ''
    }
    #print(data)
    try:
        # 发送POST请求（requests默认会将data编码为application/x-www-form-urlencoded）
        response = requests.post(url, data=user_info, headers=headers)
        time.sleep(5)

        # 检查请求是否成功
        if response.status_code == 200 and check_error(response.text):
            # 获取并打印返回的内容
            #print(response.text)
            print(f"{user_info['realname']} 添加成功!")
            return True
        else:
            #print(response.text)
            print(f"{user_info['realname']} 添加失败! 状态码：{response.status_code}")
            return False

    except requests.RequestException as e:
        # 处理请求异常
        print(f"请求过程中发生异常：{e}")
        return False

def del_all_user():
    user_count = 1
    while user_count:
        data = query_all_user_info()
        user_id_list = [d['m_id'] for d in data]
        user_count = len(user_id_list)
        print(f"use_id: {user_id_list}")
        for user_id in user_id_list:
            del_tourist(user_id)

def add_all_user(xlsx_rela_path):
    success_list = []
    fail_list = []
    user_infos = read_user_info_from_xlsx(xlsx_rela_path)
    for user_info in user_infos:
        if add_user(user_info):
            success_list.append(user_info['realname'])
        else:
            fail_list.append(user_info['realname'])

    print(f"add success: {len(success_list)}")
    print(f"add fail: {len(fail_list)}")
    print(f"fail list: {fail_list}")

def check_result(xlsx_rela_path):
    sex_dict = {
        "1": "男",
        "2": "女"
    }
    type_dict = {
        "1": "成人",
        "2": "儿童"
    }
    print("查询结果：")
    check_dict = {}
    user_info_list = query_all_user_info()
    for val in user_info_list:
        print(val)
        check_dict[val["id_number"]] = {}
        check_dict[val["id_number"]]["html_info"] = val


    user_infos = read_user_info_from_xlsx(xlsx_rela_path)
    for each in user_infos:
        if check_dict.get(each["cardno"]):
            check_dict[each["cardno"]]["excel_info"] = each
        else:
            check_dict[each["cardno"]] = {}
            check_dict[each["cardno"]]["excel_info"] = each

    index = 0
    for each in check_dict:
        index += 1
        #print(each, check_dict[each])
        data = check_dict[each]
        res_str = f"{index} check {each}"
        if not data.get("excel_info"):
            res_str += " excel表格中没有这个身份证号，请检查！"
            print(res_str)
            continue
        if not data.get("html_info"):
            res_str += " 网页中没有这个身份证号，请检查！"
            print(res_str)
            continue

        excel_name = data['excel_info']['realname']
        html_name = data['html_info']['username']
        if excel_name != html_name:
            res_str += f" excel名字：{excel_name} != {html_name}！"
            print(res_str)
            continue
        res_str += f" {excel_name}"
        if data['excel_info']['phone'] != data['html_info']['phone_number']:
            res_str += f" excel手机号：{data['excel_info']['phone']} != {data['html_info']['phone_number']}！"
            print(res_str)
            continue

        excel_sex = sex_dict.get(data['excel_info']['sex'])
        html_sex = data['html_info']['sex']
        if excel_sex != html_sex:
            res_str += f" excel性别：{excel_sex} != {html_sex}！"
            print(res_str)
            continue

        excel_type = type_dict.get(data['excel_info']['type'])
        html_type = data['html_info']['m_type']
        if excel_type != html_type:
            res_str += f" excel类型：{excel_type} != {html_type}！"
            print(res_str)
            continue

        res_str += " check success!"
        print(res_str)









if __name__ == '__main__':
    xlsx_rela_path = "11_10周日：经典_·_徽杭古道_重走徽商之路，新手必入.xlsx"
    del_all_user()
    add_all_user(xlsx_rela_path)
    check_result(xlsx_rela_path)


