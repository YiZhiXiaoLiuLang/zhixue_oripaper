# ZXOP 一个一个通过智学网api实现渲染原卷的程序

![tmp1751257309 2559702_1](https://github.com/user-attachments/assets/97fb90af-cc63-4ed4-a6a5-c90a42ff6384)


### 部署
```shell
pip39 install -r requirements.txt
python39 server.py
```

### API 服务器文档 (版本 1.5.0)

---

#### 基础信息
- **访问地址**: `http://localhost:1139`
- **认证方式**: API Token（通过URL参数`api_token`传递）
- **全局错误格式**:
  ```json
  {
    "serverversion": "1.5.0-a0+20250629.None.None",
    "error": "错误描述",
    "status": "error",
    "code": HTTP状态码
  }
  ```

---

### 1. 试卷数据获取
#### GET `/api/v1/oripaper`
获取指定用户的原始试卷数据，支持内存和文件缓存。

**请求参数**:
| 参数名        | 类型   | 必填 | 说明                                                                 |
|---------------|--------|------|----------------------------------------------------------------------|
| `userId`      | string | 是   | 用户ID（支持小ID或原始ID，小ID会自动转换）                           |
| `topicSetId`  | string | 是   | 试卷集ID                                                            |
| `api_token`   | string | 是   | 认证令牌（支持预置Token或通过`yfylyh99+userId`生成的MD5）            |

**响应**:
- 成功：HTML格式的图片画廊页面（状态码200）
- 失败：返回错误JSON（状态码400/401）

**缓存机制**:
1. 优先检查内存缓存
2. 内存未命中时检查`cache_files/`目录下的JSON缓存文件
3. 无缓存时实时生成新数据并缓存

**错误码**:
- `400`：缺少必要参数
- `401`：无效API令牌

---

### 2. Cookie管理
#### POST `/api/v2/UpdateCookie`
更新全局Cookie数据（需管理员权限）。

**请求参数**:
| 参数名      | 类型   | 必填 | 位置   | 说明                           |
|-------------|--------|------|--------|--------------------------------|
| `api_token` | string | 是   | URL    | 管理员令牌（如`admin_token`） |
| JSON数据    | dict   | 是   | Body   | 完整的Cookie字典              |

**响应示例**:
```json
{
  "status": "success",
  "message": "Cookie已更新",
  "new_data": {"cookie_key": "value"},
  "size": 123
}
```

**错误码**:
- `400`：无效JSON格式
- `401`：未授权访问

---

### 3. 日志文件管理
#### GET `/logfile`
列出日志目录中的所有文件（按修改时间倒序）。

**响应**:
HTML页面显示文件列表，包含文件名、大小和修改时间。

#### GET `/logfile/<filename>`
预览日志文件内容（限制≤2MB）。

**路径参数**:
| 参数名   | 类型   | 说明         |
|----------|--------|--------------|
| filename | string | 日志文件名   |

**响应**:
- 小文件：HTML渲染的文本内容
- 大文件：提示下载链接

#### GET `/logfile/download/<filename>`
下载日志文件。

**路径参数**:
| 参数名   | 类型   | 说明         |
|----------|--------|--------------|
| filename | string | 日志文件名   |

**响应**:
文件二进制流（`application/octet-stream`）

---

### 4. 试卷刷新接口 (危险)
#### GET `/api/v2/shuaxinsuoyoushijuan`
⚠️ **警告：未实现多线程，可能阻塞服务！**  
强制刷新所有试卷数据。

**请求参数**:
| 参数名        | 类型   | 必填 | 默认值                        | 说明              |
|---------------|--------|------|-------------------------------|-------------------|
| `api_token`   | string | 是   | -                             | 管理员令牌        |
| `topic_set_id`| string | 是   | -                             | 试卷集ID          |
| `base_url`    | string | 否   | `http://localhost:1139/api/v1/oripaper` | 数据源API地址     |

**响应**:
日志文件名称
如 `log/autogetoripaper2025-06-28-16_24_49.log`
---

### 认证令牌说明
预置有效令牌:
```python
{
  "admin_token": "testadmin114514[",    # 管理员权限
  "user_token_123": "user114514",       # 普通用户
  "test_api_key": "testtoken"           # 测试令牌
}
```
动态令牌生成公式：  
`MD5('yfylyh99' + userId)`  
例如用户ID `12345` 的令牌：  
`hashlib.md5('yfylyh9912345'.encode()).hexdigest()`

---

### 目录结构
```
├── cache_files/       # 试卷缓存目录
├── log/               # 日志存储目录
├── smalltobigid.txt   # 用户ID映射表
├── cookies.json       # Cookie存储文件
└── templates/         # HTML模板
```

---

> 最后更新：2025-06-29  
> 注意：生产环境请勿启用`debug=True`模式
