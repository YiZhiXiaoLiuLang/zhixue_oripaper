import json,requests,time
import v0
import os,time
#OUTPUT_SERVER_HOST='http://localhost:50002/'
#OUTPUT_SERVER_HOST='http://39.99.41.233:65002/'

OUTPUT_SERVER_HOST=''

cookies=json.load(open('cookies.json','r',encoding='utf-8'))
def oripaper(userId,topicSetId,savename,zxcookie=cookies):#savename不需要后缀！！！！
    global cookies
    #https://ali-bg.zhixue.com/api-classreport/class/student/getNewCheckSheet/
    #?userId=[数据删除]&topicSetId=70f25e76-b8c5-4ea7-9de7-[数据删除]
    res=requests.get(f"https://ali-bg.zhixue.com/api-classreport/class/student/getNewCheckSheet/?userId={userId}&topicSetId={topicSetId}",cookies=zxcookie)
    print(f"https://ali-bg.zhixue.com/api-classreport/class/student/getNewCheckSheet/?userId={userId}&topicSetId={topicSetId}")
    savejsonname=(f"OriPaperTMP/tmp{str(time.time())}_{userId}_{topicSetId}.json")
    with open(savejsonname,'wb') as f:
        f.write(res.content)
    file_list=v0.run(savejsonname)
    savename='output/'+savename
    uploadfilenamelist=[]
    # 遍历文件列表并重命名
    for idx, old_name in enumerate(file_list, start=1):
        # 获取文件扩展名
        ext = os.path.splitext(old_name)[1]
        # 构造新文件名
        new_name = f"{savename}_{idx}{ext}"
        # 重命名文件（假设文件在当前目录下）
        os.rename(old_name, new_name)
        print(f"Renamed '{old_name}' to '{new_name}'")
        uploadfilenamelist.append(OUTPUT_SERVER_HOST+new_name)
    return uploadfilenamelist
#oripaper("15000001002180[数据删除]","bd7b5de7-29d8-4ad7-a24c-ee8c622[数据删除]",str(time.time()))