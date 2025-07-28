import requests
import threading
import time

# 用户 ID 列表
user_ids = ['1500000100163[数据删除]', '150000010016[数据删除]', '15000001001630[数据删除]']
topicsetid_list = [
    "1f76a0fe-5221-4634-a1b6-[数据删除]",
    "ba636d72-ee65-4d5b-80fe-[数据删除]",
    "3735a3e0-9887-40d5-9af6-[数据删除]",
    "b72a1b96-ffd0-4584-af3d-[数据删除]",
    "9e5e8527-b80d-4011-9430-[数据删除]",
]
'''
for topic_set_id in topicsetid_list:
    # 接口参数
    base_url = "http://localhost:50000/api/v1/oripaper"
    #topic_set_id = "9e5e8527-b80d-4011-9430-[数据删除]"
    api_token = "test_api_key"

    # 遍历并请求接口
    for user_id in user_ids:
        params = {
            "userId": user_id,
            "topicSetId": topic_set_id,
            "api_token": api_token
        }

        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()  # 如果响应状态码不是 200，将抛出异常
            print(f"用户 {user_id} 返回结果：")
            print(response.status_code)  # 假设接口返回 JSON 数据
        except requests.exceptions.RequestException as e:
            print(f"请求用户 {user_id} 失败：{e}")
            '''
def v1(topic_set_id,base_url = "http://localhost:50000/api/v1/oripaper",api_token = "test_api_key"):

    # 获取当前时间戳
    timestamp = time.time()

    # 格式化为本地时间
    local_time = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(timestamp))
    log_file_name='log/autogetoripaper'+local_time+'.log'
    threading.Thread(target=v1_next, args=(topic_set_id,base_url,api_token,log_file_name)).start()
    
    return log_file_name
def v1_next(topic_set_id,base_url,api_token,log_file_name):
    log_file=open(log_file_name,'a',encoding='utf-8')
    #log_file.write(local_time)  # 输出类似：2023-10-01 14:30:45
    
    # 接口参数
    #base_url = "http://localhost:50000/api/v1/oripaper"
    #topic_set_id = "9e5e8527-b80d-4011-9430-[数据删除]"
    #api_token = "test_api_key"

    # 遍历并请求接口
    for user_id in user_ids:
        log_file.write(f'[{time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))}]')
        params = {
            "userId": user_id,
            "topicSetId": topic_set_id,
            "api_token": api_token
        }
        #print(params)
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()  # 如果响应状态码不是 200，将抛出异常
            log_file.write(f"用户 {user_id} 返回结果：")
            log_file.write(str(response.status_code))  # 假设接口返回 JSON 数据
        except requests.exceptions.RequestException as e:
            log_file.write(f"请求用户 {user_id} 失败：{e}")
        log_file.write('\n')
        log_file.close()
        log_file=open(log_file_name,'a',encoding='utf-8')
    
