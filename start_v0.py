import json,requests,time
import v0
import os

file_list = ['name1.png', 'name2.png']


cookies=json.load(open('cookies.json','r',encoding='utf-8'))
def oripaper(userId,topicSetId,savename):#savename不需要后缀！！！！
    global cookies
    #https://ali-bg.zhixue.com/api-classreport/class/student/getNewCheckSheet/
    #?userId=1500000100218065138&topicSetId=70f25e76-b8c5-4ea7-9de7-c39254972084
    res=requests.get(f"https://ali-bg.zhixue.com/api-classreport/class/student/getNewCheckSheet/?userId={userId}&topicSetId={topicSetId}",cookies=cookies)
    print(f"https://ali-bg.zhixue.com/api-classreport/class/student/getNewCheckSheet/?userId={userId}&topicSetId={topicSetId}")
    savejsonname=(f"tmp{str(time.time())}_{userId}_{topicSetId}.json")
    with open(savejsonname,'wb') as f:
        f.write(res.content)
    file_list=v0.run(savejsonname)
    # 遍历文件列表并重命名
    for idx, old_name in enumerate(file_list, start=1):
        # 获取文件扩展名
        ext = os.path.splitext(old_name)[1]
        # 构造新文件名
        new_name = f"{savename}_{idx}{ext}"
        # 重命名文件（假设文件在当前目录下）
        os.rename(old_name, new_name)
        print(f"Renamed '{old_name}' to '{new_name}'")
oripaper("1500000100218065139","70f25e76-b8c5-4ea7-9de7-c39254972084",'yufan')
