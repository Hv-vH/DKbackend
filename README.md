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

| 字段名      | 类型    | 描述             |
|-------------|---------|------------------|
| detail      | string  | 错误信息         |

**示例：**

```json
{
    pass
}
```

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
    pass
}
```

---