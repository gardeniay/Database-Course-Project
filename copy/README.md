# 知乎简易版系统

这是一个基于Flask的知识分享平台，用户可以发布问题、回答问题、发表文章以及浏览电子书。

## 系统功能

- 用户管理：注册、登录、修改个人信息
- 问题管理：发布问题、查看问题、回答问题
- 文章管理：发布文章、阅读文章、点赞文章
- 电子书商城：浏览电子书信息
- 创作中心：管理个人创作内容

## 技术栈

- 后端：Flask + PyMySQL
- 前端：HTML + CSS + JavaScript
- 数据库：MySQL

## 安装与配置

1. 克隆项目

```bash
git clone <repository-url>
cd <project-folder>
```

2. 创建并激活虚拟环境（推荐）

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. 安装依赖

```bash
pip install -r requirements.txt
```

4. 配置数据库

数据库连接信息可以通过环境变量配置，默认值如下：

- 数据库主机：127.0.0.1
- 数据库端口：3306
- 数据库名称：zhihu
- 数据库用户：root
- 数据库密码：928520zjf.

可以通过设置以下环境变量修改数据库连接：

```bash
# Windows
set DB_HOST=your_host
set DB_PORT=your_port
set DB_NAME=your_db_name
set DB_USER=your_username
set DB_PASSWORD=your_password

# Linux/Mac
export DB_HOST=your_host
export DB_PORT=your_port
export DB_NAME=your_db_name
export DB_USER=your_username
export DB_PASSWORD=your_password
```

5. 初始化数据库

使用提供的SQL脚本初始化数据库：

```bash
mysql -u root -p < Dump20211231.sql
```

## 启动应用

```bash
python app.py
```

应用将在 <http://127.0.0.1:8080> 上运行。

## 用户指南

### 登录系统

使用已有的用户ID登录系统。在数据库初始化后，可以使用以下示例用户ID登录：

- 普通用户：2, 4, 5, 6
- 管理员用户：1, 3, 7

### 主要功能

1. **问题界面**：查看所有问题，可以发布新问题或回答已有问题
2. **文章阅读**：浏览所有文章，可以点赞或搜索文章
3. **电子书商城**：查看电子书信息
4. **用户中心**：管理用户信息，包括注册、注销、修改和查询
5. **创作中心**：查看和管理个人创作的问题、回答和文章

## 开发说明

- `app.py`：Flask应用的主入口，包含所有路由和业务逻辑
- `static/`：存放静态资源（CSS、JavaScript等）
- `templates/`：存放HTML模板文件

## 原系统迁移说明

本系统是从原有的web.py框架迁移到Flask框架，保留了原有的功能，并对前端界面进行了优化。
