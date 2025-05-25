_VERSION='0.1.0'#主版本.次版本.补丁-hw硬件版本+日期.git哈希.crc校验
_imageAnswer_HOST='https://zhixue-sc.oss-cn-hangzhou.aliyuncs.com/'#"imageAnswer": "[\"scDV2dv_marking/scanFile/2025/05/21/AfterCorrect_oss_3a5345c6-0729-4bb8-bd2b-1ec19e4333a4A_117_882_1427_433.jpg\"]",

import json
import drawkuangkuang_v2 as drawkuangkuang_v1
from downloade_v1 import downloade
from pillowdrawtext_v1 import pillowdrawtext
import time
def run(jsonname):
    a=json.load(open(jsonname,'r',encoding='utf-8'))
    a_re=a['result']
    #print(a_re["answerSheetLocation"])
    #print(a_re["sheetDatas"])
    sheetdata=json.loads(a_re["sheetDatas"])
    sheetlocation=json.loads(a_re["answerSheetLocation"])
    kuangkuang={}
    for i in sheetdata['userAnswerRecordDTO']['answerRecordDetails']:
        #print(i)
        i['answer']
        i['dispTitle']#id（？
        i['score']#得分
        i['standardScore']#满分
        i['sourceCategoryName']#题目类型
        i['isCorrect']#是否满分，是->true，否->false
        
        kuangkuang[i['dispTitle']]={'answer':i['answer'],'score':i['score'],'standardScore':i['standardScore'],'sourceCategoryName':i['sourceCategoryName'],'isCorrect':i['isCorrect']}
        #print('---------------------')


    #canvas = create_blank_canvas(width=1118, height=1555)
    dlcfilename=[]
    for i in range(len(a_re['sheetImages'])):
        dlcfilename.append(a_re['sheetImages'][i][-16:]+'.jpg')#这里把url最后16位作为唯一标识符
        #https://zhixue-sc.oss-cn-hangzhou.aliyuncs.com/scDV2dv_marking/scanFile/2025/05/16/AfterCorrect_oss_41badd9b-ccd6-49a1-8a03-347152f84994B.jpg?Expires=1748154727&OSSAccessKeyId=LTAIdp4LguxjYLnS&Signature=x22P4wywg3DKbJEwrUg96Lk5XhU%3D
        
    downloade(a_re['sheetImages'],dlcfilename)

    pageindex=0#dlcfilename[pageindex]
    for pagesheet in sheetlocation['pageSheets']:
        rects =[]
        start_time=time.time()
        logg=['ZXOP '+_VERSION+' by chenjingshen 运行！']
        #print(pageindex,dlcfilename[pageindex])
        for i in pagesheet['sections']:
            '''
            {
                    'pTop': 0,
                    'widthPercent': 0.8398926654740608,
                    'top': 965,
                    'left': 99,
                    'width': 939,
                    'topPercent': 0.6205787781350482,
                    'pLeft': 0,
                    'ID': '36adce8f-a2ab-482c-8654-5ced6b9df562',
                    'ErrorCode': 0,
                    'leftPercent': 0.0885509838998211,
                    'height': 460,
                    'heightPercent': 0.2958199356913183
            }
            '''
            #print(i['type'],i['contents']['branch'][0]['ixList'])

            #print(i)
            addtext='\n'
            for j in i['contents']['branch'][0]['ixList']:
                if not kuangkuang[str(j)]['isCorrect']:#不是满分，题号前加感叹号
                    addtext+='!'
                addtext+=str(j)+':'+str(kuangkuang[str(j)]['score'])+'/'+str(kuangkuang[str(j)]['standardScore'])+','+str(kuangkuang[str(j)]['answer'])+'\n'
            #addtext='\n'+str(i['contents']['branch'][0]['ixList'])+'\nbalala'
            try:
                i_position=i['position']
            except:
                i_position=i['contents']['position']
                logg.append('E:题目'+str(i['contents']['branch'][0]['ixList'])+'位置获取失败，使用相对位置代替！')
            i_position['addtext']=addtext
            
            rects.append(i_position)
                
        #print(len(rects))
        logg.append('标记了'+str(len(rects))+'处地点')
        logg.append('标记完成，标记用时'+str(time.time()-start_time))
        drawkuangkuang_v1.draw_rectangles_on_canvas(rects, save_path=dlcfilename[pageindex], show=False)
        pillowdrawtext(dlcfilename[pageindex],logg, font_size=8)
 
        pageindex+=1
    return dlcfilename
