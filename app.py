from flask import Flask, render_template, request, redirect, url_for, session
import pymysql
import datetime
import os
from functools import wraps

# 创建Flask应用
app = Flask(__name__)
app.secret_key = 'simple_zhihu_secret_key'  # 用于session

# 管理员ID列表，拥有特殊权限
manister = [1, 3, 7]

# 从环境变量获取数据库配置，如果不存在则使用默认值
db_host = os.getenv('DB_HOST', '127.0.0.1')  # 数据库主机
db_port = int(os.getenv('DB_PORT', '3306'))  # MySQL默认端口是3306
db_name = os.getenv('DB_NAME', 'zhihu')  # 数据库名称
db_user = os.getenv('DB_USER', 'root')  # 数据库用户名
db_password = os.getenv('DB_PASSWORD', '928520zjf.')  # 数据库密码

# 创建数据库连接
def get_db():
    # 返回一个到MySQL的连接，使用字典游标便于数据处理
    conn = pymysql.connect(
        host=db_host,
        port=db_port,
        user=db_user,
        password=db_password,
        database=db_name,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor  # 返回字典形式的结果
    )
    return conn

# 执行查询操作
def query_db(query, args=(), one=False):
    # 执行SQL查询并返回结果，one=True时仅返回第一条记录
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(query, args)
    rv = cursor.fetchall()  # 获取所有结果
    conn.commit()
    cursor.close()
    conn.close()
    return (rv[0] if rv else None) if one else rv

# 执行插入操作
def insert_db(table, data):
    # 向指定表插入数据，data是包含字段名和值的字典
    conn = get_db()
    cursor = conn.cursor()
    
    columns = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
    
    cursor.execute(query, list(data.values()))
    last_id = cursor.lastrowid  # 获取插入记录的ID
    conn.commit()
    cursor.close()
    conn.close()
    return last_id

# 执行更新操作
def update_db(table, data, condition):
    # 更新指定表中满足条件的记录，data是要更新的字段，condition是条件
    conn = get_db()
    cursor = conn.cursor()
    
    set_clause = ', '.join([f"{key} = %s" for key in data.keys()])
    where_clause = ' AND '.join([f"{key} = %s" for key in condition.keys()])
    
    query = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
    
    cursor.execute(query, list(data.values()) + list(condition.values()))
    affected_rows = cursor.rowcount  # 获取受影响的行数
    conn.commit()
    cursor.close()
    conn.close()
    return affected_rows

# 执行删除操作
def delete_db(table, condition):
    # 从指定表中删除满足条件的记录
    conn = get_db()
    cursor = conn.cursor()
    
    where_clause = ' AND '.join([f"{key} = %s" for key in condition.keys()])
    
    query = f"DELETE FROM {table} WHERE {where_clause}"
    
    cursor.execute(query, list(condition.values()))
    affected_rows = cursor.rowcount
    conn.commit()
    cursor.close()
    conn.close()
    return affected_rows

# 检查用户是否登录的装饰器
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 如果未登录，重定向到登录页面
        if 'user_id' not in session:
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

# 首页/登录页面
@app.route('/')
def index():
    # 显示登录页面
    return render_template('login.html')

# 登录处理
@app.route('/login', methods=['POST'])
def login():
    # 处理用户登录请求
    user_id = request.form.get('用户ID')
    if not user_id:
        return redirect(url_for('index'))
    
    # 检查用户ID是否存在
    user = query_db('SELECT 用户ID FROM user WHERE 用户ID = %s', [user_id], one=True)
    
    if user:
        # 登录成功，保存用户ID到会话
        session['user_id'] = user['用户ID']
        return redirect(url_for('home_page'))
    else:
        # 登录失败，显示错误页面
        return render_template('nologin.html')

# 首页
@app.route('/shouye')
def home_page():
    # 显示应用首页
    return render_template('shouye.html')

# 返回首页
@app.route('/back_shouye', methods=['POST', 'GET'])
def back_home():
    # 从其他页面返回首页
    return render_template('shouye.html')

# 用户中心入口
@app.route('/user', methods=['POST', 'GET'])
def user():
    return redirect(url_for('user_center'))

# 用户中心页面
@app.route('/index', methods=['POST', 'GET'])
def user_center():
    return render_template('user_center.html')

# 问题相关路由
@app.route('/ask', methods=['POST', 'GET'])
def ask():
    # 跳转到问题列表页面
    return redirect(url_for('question'))

@app.route('/question')
def question():
    # 显示问题列表，按回答数降序排列
    questions = query_db('SELECT * FROM question ORDER BY 回答数 DESC')
    return render_template('question_list.html', email=questions)

@app.route('/question_check')
def question_check():
    # 检查问题详情
    questions = query_db('SELECT * FROM question')
    return render_template('question_check.html', email=questions)

@app.route('/back_question', methods=['POST', 'GET'])
def back_question():
    # 返回到问题列表
    questions = query_db('SELECT * FROM question ORDER BY 回答数 DESC')
    return render_template('question_list.html', email=questions)

@app.route('/insert_question', methods=['POST', 'GET'])
def insert_question():
    # 显示问题创建表单
    return render_template('question_add.html')

@app.route('/question_insert', methods=['POST'])
@login_required  # 需要登录才能创建问题
def question_insert():
    # 处理问题创建请求
    content = request.form.get('问题内容')
    if content == '问题内容':
        return redirect(url_for('question'))
    
    # 自动生成问题ID（获取最大ID并加1）
    max_id_result = query_db('SELECT MAX(问题ID) as max_id FROM question', one=True)
    wenti = 1 if not max_id_result or max_id_result['max_id'] is None else max_id_result['max_id'] + 1
    
    # 获取当前日期
    nowtime = datetime.datetime.now().strftime('%Y-%m-%d')
    
    # 插入新问题
    insert_db('question', {
        '问题ID': wenti,
        '提问用户ID': session['user_id'],
        '问题内容': content,
        '发布日期': nowtime,
        '回答数': 0
    })
    
    return redirect(url_for('question'))

@app.route('/delete_question', methods=['POST'])
@login_required
def delete_question():
    # 删除问题
    question_id = request.form.get('问题ID')
    delete_db('question', {'问题ID': question_id})
    
    # 获取当前用户ID
    user_id = session['user_id']
    
    # 根据用户权限返回不同内容
    if user_id not in manister:  # 非管理员只能看到自己的内容
        questions = query_db('SELECT * FROM question WHERE 提问用户ID = %s', [user_id])
        answers = query_db('SELECT * FROM answer WHERE 用户ID = %s', [user_id])
        essays = query_db('SELECT * FROM essay WHERE 文章用户ID = %s', [user_id])
    else:  # 管理员可以看到所有内容
        questions = query_db('SELECT * FROM question')
        answers = query_db('SELECT * FROM answer')
        essays = query_db('SELECT * FROM essay')
    
    return render_template('create_center.html', questions=questions, answers=answers, essays=essays)

# 回答相关路由
@app.route('/answer')
def answer():
    # 显示所有回答
    answers = query_db('SELECT * FROM answer')
    return render_template('answer_list.html', email=answers)

@app.route('/insert_answer', methods=['POST', 'GET'])
def insert_answer():
    # 显示回答创建表单
    return render_template('answer_insert.html')

@app.route('/read_answer', methods=['POST', 'GET'])
def read_answer():
    # 同时从GET和POST请求中获取参数
    question_content = request.values.get('问题内容')
    question_id = request.values.get('问题ID')
    
    # 如果有问题内容参数，则按内容搜索问题
    if question_content:
        questions = query_db("SELECT * FROM question WHERE 问题内容 LIKE %s", [f'%{question_content}%'])
        return render_template('question_check.html', questions=questions)
    
    # 如果有问题ID参数，则查看该问题下的回答
    if question_id:
        session['question_id'] = question_id  # 保存问题ID到会话，用于后续添加回答
        answers = query_db('SELECT * FROM answer WHERE 问题ID = %s ORDER BY 回答时间 DESC', [question_id])
        return render_template('answer_list.html', email=answers)
    
    return redirect(url_for('question'))

@app.route('/answer_add', methods=['POST'])
@login_required
def answer_add():
    # 处理添加回答请求
    answer_text = request.form.get('回答文本')
    question_id = session.get('question_id')
    
    if not question_id:
        return redirect(url_for('question'))
    
    # 生成新回答ID
    max_id_result = query_db('SELECT MAX(回答ID) as max_id FROM answer', one=True)
    answer_id = 1 if not max_id_result or max_id_result['max_id'] is None else max_id_result['max_id'] + 1
    
    nowtime = datetime.datetime.now().strftime('%Y-%m-%d')
    
    # 插入新回答
    insert_db('answer', {
        '回答ID': answer_id,
        '问题ID': question_id,
        '用户ID': session['user_id'],
        '回答文本': answer_text,
        '回答时间': nowtime
    })
    
    # 更新问题的回答数
    update_db('question', {'回答数': query_db('SELECT 回答数 FROM question WHERE 问题ID = %s', [question_id], one=True)['回答数'] + 1}, {'问题ID': question_id})
    
    answers = query_db('SELECT * FROM answer WHERE 问题ID = %s ORDER BY 回答时间 DESC', [question_id])
    return render_template('answer_list.html', email=answers)

@app.route('/delete_answer', methods=['POST'])
@login_required
def delete_answer():
    # 删除回答
    answer_id = request.form.get('回答ID')
    
    # 获取问题ID以便更新回答数
    answer = query_db('SELECT 问题ID FROM answer WHERE 回答ID = %s', [answer_id], one=True)
    if answer:
        question_id = answer['问题ID']
        delete_db('answer', {'回答ID': answer_id})
        
        # 更新问题的回答数
        update_db('question', {'回答数': query_db('SELECT 回答数 FROM question WHERE 问题ID = %s', [question_id], one=True)['回答数'] - 1}, {'问题ID': question_id})
    
    # 根据用户权限返回不同内容
    user_id = session['user_id']
    if user_id not in manister:
        questions = query_db('SELECT * FROM question WHERE 提问用户ID = %s', [user_id])
        answers = query_db('SELECT * FROM answer WHERE 用户ID = %s', [user_id])
        essays = query_db('SELECT * FROM essay WHERE 文章用户ID = %s', [user_id])
    else:
        questions = query_db('SELECT * FROM question')
        answers = query_db('SELECT * FROM answer')
        essays = query_db('SELECT * FROM essay')
    
    return render_template('create_center.html', questions=questions, answers=answers, essays=essays)

# 文章相关路由
@app.route('/essay', methods=['POST', 'GET'])
def essay():
    # 显示文章列表，按赞同数降序排列
    essays = query_db('SELECT * FROM essay ORDER BY 赞同数 DESC')
    return render_template('essay_list.html', email=essays)

@app.route('/passage')
def passage():
    # 另一个显示文章列表的路由
    essays = query_db('SELECT * FROM essay ORDER BY 赞同数 DESC')
    return render_template('essay_list.html', email=essays)

@app.route('/insert_essay', methods=['POST', 'GET'])
def insert_essay():
    # 显示文章创建表单
    return render_template('essay_insert.html')

@app.route('/find_essay', methods=['POST'])
def find_essay():
    # 处理文章搜索请求
    title = request.form.get('文章标题内容')
    content = request.form.get('文章内容')
    
    # 根据不同的搜索条件组合执行不同查询
    if not title and not content:
        essays = query_db('SELECT * FROM essay')
    elif title and not content:
        essays = query_db("SELECT * FROM essay WHERE 文章标题 LIKE %s", [f'%{title}%'])
    elif not title and content:
        essays = query_db("SELECT * FROM essay WHERE 文章内容 LIKE %s", [f'%{content}%'])
    else:
        essays = query_db("SELECT * FROM essay WHERE 文章内容 LIKE %s OR 文章标题 LIKE %s", [f'%{content}%', f'%{title}%'])
    
    return render_template('essay_list.html', email=essays)

@app.route('/agree', methods=['POST'])
def agree():
    # 处理文章点赞
    essay_id = request.form.get('文章ID')
    update_db('essay', {'赞同数': query_db('SELECT 赞同数 FROM essay WHERE 文章ID = %s', [essay_id], one=True)['赞同数'] + 1}, {'文章ID': essay_id})
    
    essays = query_db('SELECT * FROM essay')
    return render_template('essay_list.html', email=essays)

@app.route('/essay_add', methods=['POST'])
@login_required
def essay_add():
    # 处理添加文章请求
    title = request.form.get('文章标题')
    content = request.form.get('文章内容')
    
    if title == '文章标题' or content == '文章内容':
        return render_template('shouye.html')
    
    # 生成新文章ID
    max_id_result = query_db('SELECT MAX(文章ID) as max_id FROM essay', one=True)
    essay_id = 1 if not max_id_result or max_id_result['max_id'] is None else max_id_result['max_id'] + 1
    
    nowtime = datetime.datetime.now().strftime('%Y-%m-%d')
    
    # 插入新文章
    insert_db('essay', {
        '文章ID': essay_id,
        '文章用户ID': session['user_id'],
        '文章标题': title,
        '文章内容': content,
        '发布时间': nowtime,
        '赞同数': 0
    })
    
    essays = query_db('SELECT * FROM essay')
    return render_template('essay_list.html', email=essays)

@app.route('/delete_essay', methods=['POST'])
@login_required
def delete_essay():
    # 删除文章
    essay_id = request.form.get('文章ID')
    delete_db('essay', {'文章ID': essay_id})
    
    # 根据用户权限返回不同内容
    user_id = session['user_id']
    if user_id not in manister:
        questions = query_db('SELECT * FROM question WHERE 提问用户ID = %s', [user_id])
        answers = query_db('SELECT * FROM answer WHERE 用户ID = %s', [user_id])
        essays = query_db('SELECT * FROM essay WHERE 文章用户ID = %s', [user_id])
    else:
        questions = query_db('SELECT * FROM question')
        answers = query_db('SELECT * FROM answer')
        essays = query_db('SELECT * FROM essay')
    
    return render_template('create_center.html', questions=questions, answers=answers, essays=essays)

# 电子书相关路由
@app.route('/ebook', methods=['POST', 'GET'])
def ebook():
    # 显示电子书列表
    ebooks = query_db('SELECT * FROM ebook')
    return render_template('ebook_shop.html', email=ebooks)

@app.route('/ebook_shop')
def ebook_shop():
    # 显示电子书商店
    ebooks = query_db('SELECT * FROM ebook')
    return render_template('ebook_shop.html', email=ebooks)

# 创作中心相关路由
@app.route('/create', methods=['POST', 'GET'])
@login_required
def create():
    # 显示创作中心，根据用户身份显示不同内容
    user_id = session['user_id']
    
    if user_id not in manister:  # 非管理员只能看到自己的内容
        questions = query_db('SELECT * FROM question WHERE 提问用户ID = %s', [user_id])
        answers = query_db('SELECT * FROM answer WHERE 用户ID = %s', [user_id])
        essays = query_db('SELECT * FROM essay WHERE 文章用户ID = %s', [user_id])
    else:  # 管理员可以看到所有内容
        questions = query_db('SELECT * FROM question')
        answers = query_db('SELECT * FROM answer')
        essays = query_db('SELECT * FROM essay')
    
    return render_template('create_center.html', questions=questions, answers=answers, essays=essays)

@app.route('/create_center')
@login_required
def create_center():
    # 跳转到创作中心
    return redirect(url_for('create'))

@app.route('/center_agree', methods=['POST'])
@login_required
def center_agree():
    # 在创作中心内点赞文章
    essay_id = request.form.get('文章ID')
    update_db('essay', {'赞同数': query_db('SELECT 赞同数 FROM essay WHERE 文章ID = %s', [essay_id], one=True)['赞同数'] + 1}, {'文章ID': essay_id})
    
    # 更新创作中心的内容
    user_id = session['user_id']
    if user_id not in manister:
        questions = query_db('SELECT * FROM question WHERE 提问用户ID = %s', [user_id])
        answers = query_db('SELECT * FROM answer WHERE 用户ID = %s', [user_id])
        essays = query_db('SELECT * FROM essay WHERE 文章用户ID = %s', [user_id])
    else:
        questions = query_db('SELECT * FROM question')
        answers = query_db('SELECT * FROM answer')
        essays = query_db('SELECT * FROM essay')
    
    return render_template('create_center.html', questions=questions, answers=answers, essays=essays)

# 用户管理相关路由
@app.route('/index1')
def user_add_page():
    # 显示用户添加页面
    return render_template('user_add.html')

@app.route('/index2')
def user_delete_page():
    # 显示用户删除页面
    return render_template('user_delete.html')

@app.route('/index3')
def user_edit_page():
    # 显示用户编辑页面
    return render_template('user_edit.html')

@app.route('/index4')
def user_search_page():
    # 显示用户查询页面
    return render_template('user_search.html')

@app.route('/index5')
def user_display_page():
    # 显示用户信息页面
    users = query_db('SELECT * FROM user')
    return render_template('user_display.html', email=users)

@app.route('/turn_add', methods=['POST', 'GET'])
def turn_add():
    # 转到用户添加页面
    return redirect(url_for('user_add_page'))

@app.route('/turn_delete', methods=['POST', 'GET'])
def turn_delete():
    # 转到用户删除页面
    return redirect(url_for('user_delete_page'))

@app.route('/turn_change', methods=['POST', 'GET'])
def turn_change():
    # 转到用户修改页面
    return redirect(url_for('user_edit_page'))

@app.route('/turn_select', methods=['POST', 'GET'])
def turn_select():
    # 转到用户查询页面
    return redirect(url_for('user_search_page'))

@app.route('/add', methods=['POST'])
def add():
    # 处理添加用户请求
    user_id = request.form.get('用户ID')
    username = request.form.get('用户名')
    intro = request.form.get('个人简介')
    industry = request.form.get('所在行业')
    
    # 验证输入是否有效
    if user_id != '用户ID' and username != '用户名' and intro != '个人简介' and industry != '所在行业':
        insert_db('user', {
            '用户ID': user_id,
            '用户名': username,
            '个人简介': intro,
            '所在行业': industry
        })
    
    return redirect(url_for('index'))

@app.route('/delete', methods=['POST'])
@login_required
def delete():
    # 处理删除用户请求，用户只能删除自己的账户
    user_id = request.form.get('用户ID')
    
    if int(user_id) != session['user_id']:
        return render_template('shouye.html')
    
    delete_db('user', {'用户ID': user_id})
    session.clear()  # 清除会话
    
    return render_template('login.html')

@app.route('/change', methods=['POST'])
@login_required
def change():
    # 处理修改用户信息请求
    user_id = request.form.get('用户ID')
    username = request.form.get('用户名')
    intro = request.form.get('个人简介')
    industry = request.form.get('所在行业')
    
    update_data = {}
    
    # 只更新非默认值的字段
    if username != '用户名':
        update_data['用户名'] = username
    
    if intro != '个人简介':
        update_data['个人简介'] = intro
    
    if industry != '所在行业':
        update_data['所在行业'] = industry
    
    if update_data:
        update_db('user', update_data, {'用户ID': user_id})
    
    return redirect(url_for('index'))

@app.route('/select', methods=['POST'])
def select():
    # 处理查询用户信息请求
    user_id = request.form.get('用户ID')
    
    if user_id == '用户ID':
        # 查询所有用户
        users = query_db('SELECT * FROM user')
    else:
        # 查询特定用户
        users = query_db('SELECT * FROM user WHERE 用户ID = %s', [user_id])
    
    return render_template('user_display.html', email=users)

@app.route('/returnback', methods=['POST'])
def returnback():
    # 返回登录页面
    return redirect(url_for('index'))

# 启动服务器
if __name__ == '__main__':
    # 在本地主机的8080端口运行应用，启用调试模式
    app.run(host='127.0.0.1', port=8080, debug=True) 