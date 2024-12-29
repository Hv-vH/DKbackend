# Django REST 后端接口文档

以下是DKbackend项目的后端接口文档。描述了接口的功能、请求方法、请求参数以及返回结果。

---

## 用户登录接口

### 接口地址
`POST /acg/login/`

### 功能描述
用于用户登录，验证用户名和密码。

### 请求参数

| 参数名      | 类型    | 必填  | 描述             |
|-------------|---------|-------|------------------|
| username    | string  | 是    | 用户名           |
| password    | string  | 是    | 密码             |

### 请求示例

```json
{
    "username": "example_user",
    "password": "example_password"
}
```

### 返回结果

#### 成功响应

| 字段名      | 类型    | 描述             |
|-------------|---------|------------------|
| token       | string  | 登录成功后的令牌 |
| user        | object  | 用户信息         |
| user.id     | integer | 用户信息 ID      |
| user.username | string | 用户名         |
| user.email  | string  | 邮箱             |
| user.nickname | string | 昵称            |
| user.avatar | string  | 头像             |
| user.description | string | 个人简介      |
| user.userid | integer | 用户 ID          |

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

| 字段名   | 类型     | 描述   |
|-------|--------|------|
| messages      | string | 错误信息 |
| errors | object | 错误信息 |
|具体错误信息| string | 错误信息 |

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
| 参数名      | 类型    | 必填  | 描述             |
|-------------|---------|-------|------------------|
| username    | string  | 是    | 用户名           |
| password    | string  | 是    | 密码             |

### 请求示例

```json
{
    "username": "example_user",
    "password": "example_password"
}
```

### 返回结果

#### 成功响应

| 字段名      | 类型    | 描述             |
|-------------|---------|------------------|
| token       | string  | 注册成功后的令牌 |
| user        | object  | 用户信息         |
| user.id     | integer | 用户信息 ID      |
| user.username | string | 用户名         |
| user.email  | string  | 邮箱             |
| user.nickname | string | 昵称            |
| user.avatar | string  | 头像             |
| user.description | string | 个人简介      |
| user.userid | integer | 用户 ID          |

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

| 字段名   | 类型     | 描述   |
|-------|--------|------|
| messages      | string | 错误信息 |
| errors | object | 错误信息 |
|具体错误信息| string | 错误信息 |

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

| 参数名      | 类型    | 必填  | 描述                    |
|-------------|---------|-------|-----------------------|
| Authorization | string | 是    | `JWT <token>` 格式的认证令牌 |

### 请求示例

```
GET /acg/profile/
Authorization: JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### 返回结果

#### 成功响应

| 字段名      | 类型    | 描述      |
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

| 字段名      | 类型    | 描述             |
|-------------|---------|------------------|
| detail      | string  | 错误信息         |

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

| 参数名      | 类型    | 必填  | 描述                    |
|-------------|---------|-------|-----------------------|
| Authorization | string | 是    | `JWT <token>` 格式的认证令牌 |

### 请求参数

| 参数名      | 类型    | 必填  | 描述             |
|-------------|---------|-------|------------------|
|avatar|file|否|用户头像|
|nickname|string|否|用户昵称|
|description|string|否|用户个人简介|

### 请求示例

```json
{
    "nickname": "S6总决赛冠军",
    "description": "这个人没有介绍"
}
```

### 返回结果

#### 成功响应

| 字段名      | 类型    | 描述      |
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

| 字段名      | 类型    | 描述             |
|-------------|---------|------------------|
| detail      | string  | 错误信息         |

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
| 参数名      | 类型    | 必填 | 描述             |
|-------------|---------|----|------------------|
|posttitle|string| 是  |post标题|
|postcontent|string| 是  |post内容|
|postimages|file| 是  |post图片|
|posttags|string| 是  |post标签|


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

| 字段名      | 类型    | 描述             |
|-------------|-------|------------------|
| 错误信息      | array | 错误信息         |

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

## 关注接口

### 接口地址
- `GET /acg/follows/list/` - 获取关注列表
- `POST /acg/follows/user/` - 关注用户
- `DELETE /acg/follows/<int:user_id>/` - 取消关注

### 功能描述
- **获取关注列表**：返回当前用户关注的用户列表。
- **关注用户**：允许当前用户关注指定用户。
- **取消关注**：允许当前用户取消对指定用户的关注。

### 请求参数

#### 获取关注列表
无请求参数。

#### 关注用户
| 参数名   | 类型    | 必填  | 描述         |
|----------|---------|-------|--------------|
| userId   | integer | 是    | 要关注的用户ID |

#### 取消关注
| 参数名   | 类型    | 必填  | 描述         |
|----------|---------|-------|--------------|
| user_id  | integer | 是    | 要取消关注的用户ID |

### 请求示例

#### 关注用户
```json
{
    "userId": 123
}
```
### 返回结果

#### 成功响应

#### 获取关注列表

| 字段名              | 类型      | 描述       |
|------------------|---------|----------|
| follows          | array   | 关注的用户列表  |
| follows.id       | integer | 用户 ID    |
| follows.username | string  | 用户名      |


**示例：**

```json
{
        "id": 1,
        "username": "user1"
    },
    {
        "id": 2,
        "username": "user2"
}


```

#### 关注用户
```json
{
    "message": "Successfully followed."
}

```

#### 关注用户
```json
{
    "message": "Successfully unfollowed."
}


```
#### 失败响应

| 字段名       | 类型    | 描述            |
|-------------|-------|------------------|
| messages    | string| 错误信息          |
| errors      | object| 错误信息          | 
| 具体错误信息 | string| 错误信息          |

**示例：**

```json
{
    "messages": "用户不存在",
    "errors": {
        "userId": "指定的用户ID无效"
    }
}

```
---
## 点赞接口

### 接口地址
- `POST /like/post/<int:post_id>/` - 点赞动态
- `POST /like/article/<int:article_id>/` - 点赞文章
- `POST /like/comment/<int:comment_id>/` - 点赞评论

### 功能描述
- **点赞动态**：允许用户对指定动态进行点赞。
- **点赞文章**：允许用户对指定文章进行点赞。
- **点赞评论**：允许用户对指定评论进行点赞。

### 请求参数

#### 点赞动态
| 参数名   | 类型    | 必填  | 描述         |
|----------|---------|-------|--------------|
| post_id  | integer | 是    | 要点赞的动态ID |

#### 点赞文章
| 参数名   | 类型    | 必填  | 描述         |
|----------|---------|-------|--------------|
| article_id | integer | 是  | 要点赞的文章ID |

#### 点赞评论
| 参数名   | 类型    | 必填  | 描述         |
|----------|---------|-------|--------------|
| comment_id | integer | 是  | 要点赞的评论ID |

### 请求示例

#### 点赞动态
```http
POST /like/post/1/
```

**请求体示例：**
```json
{
    "userId": 123
}
```

#### 点赞文章
```http
POST /like/article/1/
```

**请求体示例：**
```json
{
    "userId": 123
}
```

#### 点赞评论
```http
POST /like/comment/1/
```

**请求体示例：**
```json
{
    "userId": 123
}
```

### 返回结果

#### 成功响应

#### 点赞成功
```json
{
    "detail": "点赞成功"
}
```

#### 失败相应

#### 已经点赞过
```json
{
    "detail": "您已经点赞过了"
}
```

#### 已经点赞过
```json
{
    "detail": "您已经点赞过了"
}
```

#### 动态未找到
```json
{
    "detail": "动态未找到"
}
```

#### 文章未找到
```json
{
    "detail": "文章未找到"
}
```

#### 评论未找到
```json
{
    "detail": "评论未找到"
}
```

## 收藏接口

### 接口地址
- `POST /posts/<int:post_id>/collect/` - 收藏帖子
- `DELETE /posts/<int:post_id>/uncollect/` - 取消收藏帖子
- `POST /articles/<int:article_id>/collect/` - 收藏文章
- `DELETE /articles/<int:article_id>/uncollect/` - 取消收藏文章

### 功能描述
- **收藏帖子**：允许用户收藏指定的帖子。
- **取消收藏帖子**：允许用户取消对指定帖子的收藏。
- **收藏文章**：允许用户收藏指定的文章。
- **取消收藏文章**：允许用户取消对指定文章的收藏。

### 请求参数

#### 收藏帖子
| 参数名   | 类型    | 必填  | 描述         |
|----------|---------|-------|--------------|
| post_id  | integer | 是    | 要收藏的帖子ID |

#### 取消收藏帖子
| 参数名   | 类型    | 必填  | 描述         |
|----------|---------|-------|--------------|
| post_id  | integer | 是    | 要取消收藏的帖子ID |

#### 收藏文章
| 参数名   | 类型    | 必填  | 描述         |
|----------|---------|-------|--------------|
| article_id | integer | 是  | 要收藏的文章ID |

#### 取消收藏文章
| 参数名   | 类型    | 必填  | 描述         |
|----------|---------|-------|--------------|
| article_id | integer | 是  | 要取消收藏的文章ID |

### 请求示例

#### 收藏帖子
```http
POST /posts/1/collect/
```

#### 取消收藏帖子
```http
DELETE /posts/1/uncollect/
```

#### 收藏文章
```http
POST /articles/1/collect/
```

#### 取消收藏文章
```http
DELETE /articles/1/uncollect/
```

### 返回结果

#### 成功响应

#### 收藏成功
```json
{
    "detail": "收藏成功"
}
```

#### 取消收藏成功
```json
{
    "detail": "取消收藏成功"
}
```
#### 失败响应

#### 已经收藏过
```json
{
    "detail": "已经收藏过"
}
```

#### 动态未找到
```json
{
    "detail": "动态未找到"
}
```

#### 文章未找到
```json
{
    "detail": "文章未找到"
}
```

#### 尚未收藏
```json
{
    "detail": "您尚未收藏此动态"
}
```

#### 尚未收藏文章
```json
{
    "detail": "尚未收藏文章"
}
```

## 用户统计接口

### 接口地址
- `GET /user/stats/<int:user_id>/` - 获取用户统计信息

### 功能描述
- **获取用户统计信息**：返回指定用户的被关注数量、关注数量和收藏数量。

### 请求参数

| 参数名   | 类型    | 必填  | 描述         |
|----------|---------|-------|--------------|
| user_id  | integer | 是    | 用户的 ID    |

### 请求示例
```http
GET /user/stats/1/
```

### 返回结果

#### 成功响应

```json
{
    "followers_count": 10,
    "following_count": 5,
    "collections_count": 3
}
```


#### 失败响应

##### 用户未找到

```json
{
    "detail": "用户未找到"
}
```


### 注意事项
- 确保提供有效的 `user_id`。
- 返回的统计信息包括：
  - `followers_count`：被关注的数量
  - `following_count`：关注的数量 
  - `collections_count`：收藏的数量

