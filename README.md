# Django REST 后端接口文档

以下是DKbackend项目的后端接口文档。描述了接口的功能、请求方法、请求参数以及返回结果。

---

## 用户登录接口

### 接口地址
`POST /acg/login/`

### 功能描述
用于用户登录，验证用户名和密码。

### 请求参数

| 参数名      | 类型     | 必填 | 描述  |
|----------|--------|----|-----|
| username | string | 是  | 用户名 |
| password | string | 是  | 密码  |

### 请求示例

```json
{
    "username": "example_user",
    "password": "example_password"
}
```

### 返回结果

#### 成功响应

| 字段名              | 类型      | 描述       |
|------------------|---------|----------|
| token            | string  | 登录成功后的令牌 |
| user             | object  | 用户信息     |
| user.id          | integer | 用户信息 ID  |
| user.username    | string  | 用户名      |
| user.email       | string  | 邮箱       |
| user.nickname    | string  | 昵称       |
| user.avatar      | string  | 头像       |
| user.description | string  | 个人简介     |
| user.userid      | integer | 用户 ID    |

**示例：**

```json
{
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "user": {
        "id": 99,
        "username": "jj",
        "email": "123@456.com",
        "nickname": "sdf",
        "avatar": "src/avatar/01837636.jpg",
        "description": "我最喜欢的动漫是《海贼王》",
        "userid": 3
    }
}
```

<img src="/png/success_login.png" alt="成功登陆图片"/>

#### 失败响应

| 字段名      | 类型     | 描述   |
|----------|--------|------|
| messages | string | 错误信息 |
| errors   | object | 错误信息 |
| 具体错误信息   | string | 错误信息 |

**示例：**

```json
{
    "messages": "参数验证失败",
    "errors": {
        "non_field_errors": [
            "密码错误"
        ]
    }
}
```
<img src="png/fail_login.png" alt="失败登陆的图片"/>

---
## 用户注册接口

### 接口地址
`POST /acg/register/`

### 功能描述
用于用户注册。

### 请求参数
| 参数名      | 类型     | 必填 | 描述  |
|----------|--------|----|-----|
| username | string | 是  | 用户名 |
| password | string | 是  | 密码  |

### 请求示例

```json
{
    "username": "example_user",
    "password": "example_password"
}
```

### 返回结果

#### 成功响应

| 字段名              | 类型      | 描述       |
|------------------|---------|----------|
| token            | string  | 注册成功后的令牌 |
| user             | object  | 用户信息     |
| user.id          | integer | 用户信息 ID  |
| user.username    | string  | 用户名      |
| user.email       | string  | 邮箱       |
| user.nickname    | string  | 昵称       |
| user.avatar      | string  | 头像       |
| user.description | string  | 个人简介     |
| user.userid      | integer | 用户 ID    |

**示例：**

```json
{
      "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyaWQiOjExLCJleHAiOjE3MzU5ODYwMjguNDk2NzAzfQ.zsGhPM-R45z7_m8Y9PTzRNtnsJIYpkpTIRaejCo7NsY",
    "user": {
        "id": 10,
        "username": "user23",
        "email": "",
        "nickname": "用户10076078296",
        "avatar": "avatars/avatar.jpg",
        "description": "",
        "userid": 11
    }
}
```
<img src="/png/success_register.png" alt="成功注册图片"/>

#### 失败响应

| 字段名      | 类型     | 描述   |
|----------|--------|------|
| messages | string | 错误信息 |
| errors   | object | 错误信息 |
| 具体错误信息   | string | 错误信息 |

**示例：**

```json
{
  "messages": "参数验证失败",
  "errors": {
        "non_field_errors": [
            "用户名已存在"
        ]
    }
}
```
<img src="/png/fail_register.png" alt="失败注册图片"/>

---
## 获取用户信息接口

### 接口地址
`GET /acg/profile/`

### 功能描述
获取当前登录用户的信息。

### 请求头部

| 参数名           | 类型     | 必填 | 描述                    |
|---------------|--------|----|-----------------------|
| Authorization | string | 是  | `JWT <token>` 格式的认证令牌 |

### 请求示例

```
GET /acg/profile/
Authorization: JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### 返回结果

#### 成功响应

| 字段名         | 类型      | 描述      |
|-------------|---------|---------|
| id          | integer | 用户信息 ID |
| username    | string  | 用户名     |
| email       | string  | 邮箱      |
| nickname    | string  | 昵称      |
| avatar      | string  | 头像      |
| description | string  | 个人简介    |
| userid      | integer | 用户 ID   |

**示例：**

```json
{
    "id": 1,
    "username": "hfdd",
    "email": "",
    "nickname": "S6总决赛冠军",
    "avatar": "src/1.jpg",
    "description": "这个人没有介绍",
    "userid": 1
}
```
<img src="/png/success_profile.png" alt="成功获取用户信息图片"/>

#### 失败响应

| 字段名    | 类型     | 描述   |
|--------|--------|------|
| detail | string | 错误信息 |

**示例：**

```json
{
   "detail": "请先登录"
}
```
<img src="/png/fail_profile.png" alt="失败获取用户信息图片"/>

---
## 修改用户信息接口

### 接口地址
`PUT /acg/profile/`

### 功能描述
修改当前登录用户的信息。

### 请求头部

| 参数名           | 类型     | 必填 | 描述                    |
|---------------|--------|----|-----------------------|
| Authorization | string | 是  | `JWT <token>` 格式的认证令牌 |

### 请求参数

| 参数名         | 类型     | 必填 | 描述     |
|-------------|--------|----|--------|
| avatar      | file   | 否  | 用户头像   |
| nickname    | string | 否  | 用户昵称   |
| description | string | 否  | 用户个人简介 |

### 请求示例

```json
{
    "nickname": "S6总决赛冠军",
    "description": "这个人没有介绍"
}
```

### 返回结果

#### 成功响应

| 字段名         | 类型      | 描述      |
|-------------|---------|---------|
| id          | integer | 用户信息 ID |
| username    | string  | 用户名     |
| email       | string  | 邮箱      |
| nickname    | string  | 昵称      |
| avatar      | string  | 头像      |
| description | string  | 个人简介    |
| userid      | integer | 用户 ID   |

**示例：**

```json
{
    "id": 1,
    "username": "hfdd",
    "email": "",
    "nickname": "S6总决赛冠军",
    "avatar": "src/1.jpg",
    "description": "这个人没有介绍",
    "userid": 1
}
```

<img src="/png/success_put_profile.png" alt="成功修改用户信息图片"/>

#### 失败响应

| 字段名    | 类型     | 描述   |
|--------|--------|------|
| detail | string | 错误信息 |

**示例：**

```json
{
   "detail": "请先登录"
}
```

<img src="/png/fail_put_profile.png" alt="失败修改用户信息图片"/>

---
## 获取post接口

### 接口地址
`GET /acg/post/`获取post列表

`GET /acg/post/<int:post_id>/`获取指定ID的post

`GET /acg/post/?search=<str:search>`标题和内容中带有搜索关键字的post列表

`GET /acg/post/?category=<str:category>`标签中带有分类关键字的post列表

### 功能描述
获取post的list 或者 某个指定ID的post 或者 搜索关键字的post 或者 分类关键字的post

### 请求头部

因为未登录用户也可以查看post，所以在前段没有存放token时，可以不带token访问

### 返回结果

#### 成功响应

| 字段名              | 类型      | 描述       |
|------------------|---------|----------|
| id               | integer | post ID  |
| userid           | integer | 用户 ID    |
| username         | string  | 用户名      |
| email            | string  | 邮箱       |
| nickname         | string  | 昵称       |
| avatar           | string  | 头像       |
| description      | string  | 个人简介     |
| posttitle        | string  | post标题   |
| postcontent      | string  | post内容   |
| postcreated_time | string  | post创建时间 |
| postimages       | string  | post图片   |
| posttags         | string  | post标签   |
| like_count       | integer | 点赞数      |
| collect_count    | integer | 收藏数      |
| comment_count    | integer | 评论数      |
| is_like          | boolean | 是否点赞     |
| is_collect       | boolean | 是否收藏     |

**示例：**

```json
{        
  "id": 1,
  "userid": 3,
  "username": "user100",
  "email": "",
  "nickname": "北京队",
  "avatar": "avatars/avatar.jpg",
  "description": "",
  "posttitle": "今天终于收到了期待已久的《鬼灭之刃》..",
  "postcontent": "最近入手了一个新的手办，质量非常好，大家看看怎么样？",
  "postcreated_time": "2024-12-17T20:51:06",
  "postimages": "['/src/assets/post1.png','/src/assets/post2.png','/src/assets/post3.png']",
  "posttags": "['手办', '鬼灭之刃', '开箱']",
  "like_count": 3,
  "collect_count": 2,
  "comment_count": 8,
  "is_like": true,
  "is_collect": false
}
```

<img src="/png/success_post.png" alt="成功获取post图片"/>

#### 失败响应

没有做处理，只可能后端报错

---
## 发布post接口

### 接口地址
`POST /acg/post/`

### 功能描述
发布post

### 请求头部 因为只有登录用户才能发表，所以必须有token
| 参数名           | 类型     | 必填 | 描述                    |
|---------------|--------|----|-----------------------|
| Authorization | string | 是  | `JWT <token>` 格式的认证令牌 |

### 请求参数
| 参数名         | 类型     | 必填 | 描述     |
|-------------|--------|----|--------|
| posttitle   | string | 是  | post标题 |
| postcontent | string | 是  | post内容 |
| postimages  | file   | 是  | post图片 |
| posttags    | string | 是  | post标签 |


### 请求示例

```json
{
    "posttitle": "今天终于收到了期待已久的《鬼灭之刃》..",
    "postcontent": "最近入手了一个新的手办，质量非常好，大家看看怎么样？",
    "postimages": "['/src/assets/post1.png','/src/assets/post2.png','/src/assets/post3.png']",
    "posttags": "['手办', '鬼灭之刃', '开箱']"
}
```

### 返回结果

#### 成功响应

| 字段名              | 类型      | 描述       |
|------------------|---------|----------|
| id               | integer | post ID  |
| userid           | integer | 用户 ID    |
| username         | string  | 用户名      |
| email            | string  | 邮箱       |
| nickname         | string  | 昵称       |
| avatar           | string  | 头像       |
| description      | string  | 个人简介     |
| posttitle        | string  | post标题   |
| postcontent      | string  | post内容   |
| postcreated_time | string  | post创建时间 |
| postimages       | string  | post图片   |
| posttags         | string  | post标签   |
| like_count       | integer | 点赞数      |
| collect_count    | integer | 收藏数      |
| comment_count    | integer | 评论数      |
| is_like          | boolean | 是否点赞     |
| is_collect       | boolean | 是否收藏     |

**示例：**

```json
{        
   "id": 7,
    "userid": 1,
    "username": "hfdd",
    "email": "",
    "nickname": "测速接口名字",
    "avatar": "测速接口头像",
    "description": "测试接口介绍",
    "posttitle": "post动态测试标题",
    "postcontent": "post动态测试内容",
    "postcreated_time": "2024-12-28T11:04:28.582751",
    "postimages": "['/cs/tupian.jpg']",
    "posttags": "['阿里云']",
    "like_count": 0,
    "collect_count": 0,
    "comment_count": 0,
    "is_like": false,
    "is_collect": false
}
```
<img src="/png/success_post_post.png" alt="成功发布post图片"/>

#### 失败响应

| 字段名  | 类型    | 描述   |
|------|-------|------|
| 错误信息 | array | 错误信息 |

**示例：**

```json
{
    "postcontent": [
        "该字段是必填项。"
    ],
    "postimages": [
        "该字段是必填项。"
    ]
}
```

<img src="/png/fail_post_post.png" alt="失败发布post图片"/>

---
## 获取评论接口

### 接口地址
`GET /acg/comment/?type=<str:type>&id=<int:id>`获取指定post类型或者article类型的评论

### 功能描述
获取post或者article的评论

### 请求头部
| 参数名           | 类型     | 必填 | 描述                    |
|---------------|--------|----|-----------------------|
| Authorization | string | 是  | `JWT <token>` 格式的认证令牌 |


### 返回结果

#### 成功响应

| 字段名                 | 类型          | 描述            |
|---------------------|-------------|---------------|
| id                  | integer     | 评论 ID         |
| userid              | integer     | 用户 ID         |
| username            | string      | 用户名           |
| email               | string      | 邮箱            |
| nickname            | string      | 昵称            |
| avatar              | string      | 头像            |
| description         | string      | 个人简介          |
| commenttype         | string      | 评论类型          |
| postid              | int         | 评论的post ID    |
| articleid           | int         | 评论的article ID |
| commentid           | int         | 评论的评论 ID      |
| commentcontent      | string      | 评论内容          |
| commentcreated_time | string      | 评论创建时间        |
| like_count          | integer     | 点赞数           |
| is_like             | boolean     | 是否点赞          |
| replies             | array[self] | 回复列表          |

**示例：**

```json
{
    "id": 1,
    "userid": 3,
    "username": "user100",
    "email": "",
    "nickname": "北京队",
    "avatar": "avatars/avatar.jpg",
    "description": "",
    "commenttype": "post",
    "postid": 1,
    "articleid": null,
    "commentid": null,
    "commentcontent": "这个手办真的很好看",
    "commentcreated_time": "2024-12-17T20:51:06",
    "like_count": 3,
    "is_like": true,
    "replies": [
        {
            "id": 2,
            "userid": 1,
            "username": "hfdd",
            "email": "",
            "nickname": "测速接口名字",
            "avatar": "测速接口头像",
            "description": "测试接口介绍",
            "commenttype": "post",
            "postid": 1,
            "articleid": null,
            "commentid": 1,
            "commentcontent": "谢谢你的夸奖",
            "commentcreated_time": "2024-12-17T20:51:06",
            "like_count": 0,
            "is_like": false,
            "replies": null
        }
    ]
}
```

<img src="/png/success_comment.png" alt="成功获取评论图片"/>

#### 失败响应

| 字段名  | 类型  | 描述   |
|------|-----|------|
| 错误信息 | str | 错误信息 |

**示例：**

```json
{
    "message": "参数错误"
}
```

<img src="/png/fail_comment.png" alt="失败获取评论图片"/>








## 发表评论接口

### 接口地址
`POST /acg/comment/`

### 功能描述
对post或者article或者评论进行评论

### 请求头部
| 参数名           | 类型     | 必填 | 描述                    |
|---------------|--------|----|-----------------------|
| Authorization | string | 是  | `JWT <token>` 格式的认证令牌 |

### 请求参数
| 参数名         | 类型     | 必填 | 描述     |
|-------------|--------|----|--------|
| commenttype | string | 是  | 评论类型   |
| postid      | int    | 否  | 评论的post ID |
| articleid   | int    | 否  | 评论的article ID |
| commentid   | int    | 否  | 评论的评论 ID |
| commentcontent | string | 是  | 评论内容 |

### 请求示例

```json
{
    "commenttype": "post",
    "postid": 1,
    "commentcontent": "这个手办真的很好看"
}
```

### 返回结果

#### 成功响应

| 字段名                 | 类型          | 描述            |
|---------------------|-------------|---------------|
| id                  | integer     | 评论 ID         |
| userid              | integer     | 用户 ID         |
| username            | string      | 用户名           |
| email               | string      | 邮箱            |
| nickname            | string      | 昵称            |
| avatar              | string      | 头像            |
| description         | string      | 个人简介          |
| ｜ postid            | int         | 评论的post ID    |
| articleid           | int         | 评论的article ID |
| commentid           | int         | 评论的评论 ID      |
| ｜commentcontent     | string      | 评论内容          |
| commentcreated_time | string      | 评论创建时间        |
| ｜like_count         | integer     | 点赞数           |
| is_like             | boolean     | 是否点赞          |
| replies             | array[self] | 回复列表          |

**示例：**

```json
{
    "id": 1,
    "userid": 3,
    "username": "user100",
    "email": "",
    "nickname": "北京队",
    "avatar": "avatars/avatar.jpg",
    "description": "",
    "commenttype": "post",
    "postid": 1,
    "articleid": null,
    "commentid": null,
    "commentcontent": "这个手办真的很好看",
    "commentcreated_time": "2024-12-17T20:51:06",
    "like_count": 3,
    "is_like": true,
    "replies": null
}
```

<img src="/png/success_post_comment.png" alt="成功评论图片"/>

#### 失败响应

| 字段名  | 类型  | 描述   |
|------|-----|------|
| 错误信息 | str | 错误信息 |

**示例：**

```json
{
    "non_field_errors": [
        "commentid不为空时，commenttype必须为comment"
    ]
}
```

<img src="/png/fail_post_comment.png" alt="失败评论图片"/>

---
