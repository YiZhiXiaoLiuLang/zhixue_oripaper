_VERSION = '1.5.0-a0+20250629.None.None'
#555
from flask import Flask, jsonify, request, abort
from start_v0 import oripaper
import time
import modhtml
import hashlib
import os,threading
import json
import os
from flask import Flask, render_template, send_from_directory, abort, request
import autogetapiv1_oripaper
IS_LITE_SERVER=False
stubigid={}
zxcookie=json.load(open('cookies.json','r',encoding='utf-8'))
with open('smalltobigid.txt',encoding='utf-8') as f:
    stubigid=json.load(f)

app = Flask('zxop_api_server')

VALID_TOKENS = {
    "admin_token": "testadmin114514[",
    "user_token_123": "user114514",
    "test_api_key": "testtoken"
}
def smallidtouserid(smallid):
    return stubigid[smallid]
        
# 缓存和缓存目录
result_cache = {}
CACHE_DIR = "cache_files"
os.makedirs(CACHE_DIR, exist_ok=True)  # 保证缓存目录存在
LOG_FOLDER = 'log'


def is_valid_token(api_token, user_id):
    if api_token in VALID_TOKENS:
        return True
    if user_id:
        user_md5 = hashlib.md5(('yfylyh99'+user_id).encode('utf-8')).hexdigest()
        if api_token.lower() == user_md5.lower():
            return True
    return False

def get_cache_file_path(user_id, topic_set_id):
    filename = f"{user_id}_{topic_set_id}.json"
    return os.path.join(CACHE_DIR, filename)
@app.route('/logfile')
def list_log_files():
    """列出日志文件夹中的所有文件"""
    try:
        # 获取日志文件夹中的所有文件
        files = os.listdir(LOG_FOLDER)
        # 过滤掉目录，只保留文件
        files = [f for f in files if os.path.isfile(os.path.join(LOG_FOLDER, f))]
        # 按修改时间排序（最新在前）
        files.sort(key=lambda x: os.path.getmtime(os.path.join(LOG_FOLDER, x)), reverse=True)
        return render_template('log_file_list.html', files=files)
    except FileNotFoundError:
        abort(404, description="日志目录不存在")
@app.route('/logfile/download/<path:filename>')
def download_file(filename):
    """下载日志文件"""
    return send_from_directory(
        LOG_FOLDER,
        filename,
        as_attachment=True,
        mimetype='application/octet-stream'
    )
@app.route('/logfile/<path:filename>')
def preview_log_file(filename):
    """预览日志文件内容"""
    # 安全检查：防止路径遍历攻击
    if '..' in filename or filename.startswith('/'):
        abort(400, description="无效的文件名")
    
    filepath = os.path.join(LOG_FOLDER, filename)
    
    # 检查文件是否存在且是普通文件
    if not os.path.isfile(filepath):
        abort(404, description="文件未找到")
    
    # 检查文件大小（超过2MB则拒绝）
    if os.path.getsize(filepath) > 2 * 1024 * 1024:
        return render_template('log_error.html', 
                              message="文件过大（超过2MB），请下载查看",
                              filename=filename)
    
    # 读取文件内容
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        # 处理二进制文件
        return render_template('log_error.html', 
                              message="无法预览二进制文件",
                              filename=filename)
    
    # 获取文件信息
    file_stats = os.stat(filepath)
    return render_template('log_preview.html', 
                          filename=filename,
                          content=content,
                          size=file_stats.st_size,
                          mtime=file_stats.st_mtime)


@app.route('/api/v2/shuaxinsuoyoushijuan', methods=['GET'])
def refresh_all_papers():
    """
    不要用啊啊啊啊没写多线程别用啊啊啊啊啊啊
    """
    # 验证API令牌
    api_token = request.args.get('api_token')
    topic_set_id = request.args.get('topic_set_id')
    if not api_token or not is_valid_token(api_token,'userid不填'):
        abort(401, description="无效的API令牌")
    
    # 获取可选的base_url参数
    base_url = request.args.get('base_url', "http://localhost:1139/api/v1/oripaper")
    
    # 调用刷新函数
    result = autogetapiv1_oripaper.v1(topic_set_id, base_url=base_url)
    
    return result
@app.route('/api/v2/UpdateCookie', methods=['POST'])
def update_cookie():
    global zxcookie
    
    # 获取并验证API令牌
    api_token = request.args.get('api_token')
    if not api_token or not is_valid_token(api_token,'userid不填'):
        abort(401, description="无效的API令牌")
    
    # 获取并解析JSON数据
    try:
        new_data = request.get_json()
        if not isinstance(new_data, dict):
            raise ValueError("数据必须是JSON对象")
    except Exception as e:
        abort(400, description=f"无效的JSON数据: {str(e)}")
    
    # 更新全局变量（直接赋值，无需锁）
    zxcookie = new_data
    
    # 返回成功响应
    return jsonify({
        "status": "success",
        "message": "Cookie已更新",
        "new_data": zxcookie,
        "size": len(json.dumps(zxcookie))
    })
@app.route('/api/v2/ViewCookie', methods=['GET'])
def view_cookie():
    global zxcookie
    
    # 获取并验证API令牌
    api_token = request.args.get('api_token')
    if not api_token or not is_valid_token(api_token,'userid不填'):
        abort(401, description="无效的API令牌")

    # 返回成功响应
    return jsonify({
        "status": "success",
        "message": "okokokk",
        "data": zxcookie,
        "size": len(json.dumps(zxcookie))
    })

@app.route('/api/v1/oripaper', methods=['GET'])
def handle_oripaper():
    global zxcookie
    user_id = request.args.get('userId')
    topic_set_id = request.args.get('topicSetId')
    api_token = request.args.get('api_token')

    if not all([user_id, topic_set_id, api_token]):
        abort(400, description="缺少必要参数: userId, topicSetId 或 api_token")

    if not is_valid_token(api_token, user_id):
        abort(401, description="无效的API令牌")
    print(user_id)
    if len(user_id)<=10:
        user_id=smallidtouserid(user_id)
        print(user_id)
    cache_key = (user_id, topic_set_id)

    # 优先内存缓存
    if cache_key in result_cache:
        result = result_cache[cache_key]

    else:
        # 检查文件缓存
        cache_file = get_cache_file_path(user_id, topic_set_id)
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    result = json.load(f)
                result_cache[cache_key] = result
            except Exception as e:
                print(f"读取缓存文件失败: {e}")
                result = None
        else:
            result = None
        
        # 如果没有缓存，生成并保存
        if not result:
            if IS_LITE_SERVER:
                return 'E:此服务端不支持获取未缓存的试卷'
            
            temp_dir = f'tmp{str(time.time())}'
            result = oripaper(user_id, topic_set_id, temp_dir,zxcookie=zxcookie)
            result_cache[cache_key] = result

            # 写入缓存文件
            try:
                with open(cache_file, 'w', encoding='utf-8') as f:
                    json.dump(result, f, ensure_ascii=False, indent=2)
            except Exception as e:
                print(f"写入缓存文件失败: {e}")
            
    return modhtml.generate_image_gallery(result,OUTPUT_SERVER_HOST='http://39.99.41.233:6502/')


@app.errorhandler(400)
@app.errorhandler(401)
@app.errorhandler(500)
def handle_errors(error):
    response = {
        "serverversion": _VERSION,
        "error": error.description,
        "status": "error",
        "code": error.code
    }
    return jsonify(response), error.code

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=1139, debug=True)
