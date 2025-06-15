# 导入必要的库
from flask import Flask, render_template, request, redirect, url_for, session  # Flask框架相关模块
import pymysql  # MySQL数据库连接模块
import datetime  # 日期时间处理模块
import os  # 操作系统相关模块
from functools import wraps  # 装饰器工具模块
from dbutils.pooled_db import PooledDB  # 数据库连接池

# 创建Flask应用实例
app = Flask(__name__)
app.secret_key = 'simple_zhihu_secret_key'  # 设置session密钥，用于会话管理

# 定义管理员ID列表，这些用户拥有特殊权限
manister = [1, 3, 7]

# 数据库配置信息
# 从环境变量获取配置，如果不存在则使用默认值
db_host = os.getenv('DB_HOST', '127.0.0.1')  # 数据库主机地址
db_port = int(os.getenv('DB_PORT', '3306'))  # 数据库端口号
db_name = os.getenv('DB_NAME', 'zhihu')  # 数据库名称
db_user = os.getenv('DB_USER', 'root')  # 数据库用户名
db_password = os.getenv('DB_PASSWORD', '928520zjf.')  # 数据库密码

# 创建数据库连接池
pool = PooledDB(
    creator=pymysql,
    maxconnections=6,  # 连接池最大连接数
    mincached=2,       # 初始化时创建的连接数
    maxcached=5,       # 连接池最大空闲连接数
    blocking=True,     # 连接池中如果没有可用连接后是否阻塞等待
    host=db_host,
    port=db_port,
    user=db_user,
    password=db_password,
    database=db_name,
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

def get_db():
    """从连接池获取数据库连接
    
    Returns:
        pymysql.connections.Connection: 返回一个配置好的数据库连接对象
    """
    return pool.connection()

def query_db(query, args=(), one=False, page=None, page_size=None):
    """执行SQL查询并返回结果
    
    Args:
        query (str): SQL查询语句
        args (tuple): 查询参数
        one (bool): 是否只返回第一条记录
        page (int): 页码，从1开始
        page_size (int): 每页记录数
        
    Returns:
        list|dict: 查询结果，如果one=True则返回单条记录，否则返回记录列表
    """
    conn = get_db()
    cursor = conn.cursor()
    
    # 添加分页
    if page is not None and page_size is not None:
        offset = (page - 1) * page_size
        query += f" LIMIT {page_size} OFFSET {offset}"
    
    cursor.execute(query, args)
    rv = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return (rv[0] if rv else None) if one else rv

def insert_db(table, data):
    """向指定表中插入数据
    
    Args:
        table (str): 目标表名
        data (dict): 要插入的数据，键为字段名，值为字段值
        
    Returns:
        int: 返回插入记录的ID
    """
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

def update_db(table, data, condition):
    """更新指定表中满足条件的记录
    
    Args:
        table (str): 目标表名
        data (dict): 要更新的字段和值
        condition (dict): 更新条件
        
    Returns:
        int: 返回受影响的行数
    """
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

def delete_db(table, condition):
    """从指定表中删除满足条件的记录
    
    Args:
        table (str): 目标表名
        condition (dict): 删除条件
        
    Returns:
        int: 返回受影响的行数
    """
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

def login_required(f):
    """检查用户是否登录的装饰器
    
    Args:
        f (function): 需要登录才能访问的视图函数
        
    Returns:
        function: 装饰后的函数，未登录时重定向到登录页面
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    """首页/登录页面路由
    
    Returns:
        str: 返回登录页面的HTML内容
    """
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    """处理用户登录请求
    
    Returns:
        Response: 登录成功重定向到首页，失败则显示错误页面
    """
    user_id = request.form.get('用户ID')
    if not user_id:
        return redirect(url_for('index'))
    
    user = query_db('SELECT 用户ID FROM user WHERE 用户ID = %s', [user_id], one=True)
    
    if user:
        session['user_id'] = user['用户ID']
        return redirect(url_for('home_page'))
    else:
        return render_template('nologin.html')

@app.route('/shouye')
def home_page():
    """应用首页路由
    
    Returns:
        str: 返回首页的HTML内容
    """
    return render_template('shouye.html')

@app.route('/back_shouye', methods=['POST', 'GET'])
def back_home():
    """返回首页的路由
    
    Returns:
        str: 返回首页的HTML内容
    """
    return render_template('shouye.html')

@app.route('/user', methods=['POST', 'GET'])
def user():
    """用户中心入口路由
    
    Returns:
        Response: 重定向到用户中心页面
    """
    return redirect(url_for('user_center'))

@app.route('/index', methods=['POST', 'GET'])
def user_center():
    """用户中心页面路由
    
    Returns:
        str: 返回用户中心页面的HTML内容
    """
    return render_template('user_center.html')

@app.route('/ask', methods=['POST', 'GET'])
def ask():
    """问题相关路由入口
    
    Returns:
        Response: 重定向到问题列表页面
    """
    return redirect(url_for('question'))

@app.route('/question')
def question():
    """显示问题列表页面
    
    Returns:
        str: 返回问题列表页面的HTML内容，包含按回答数降序排列的问题列表
    """
    page = request.args.get('page', 1, type=int)
    page_size = 10
    
    # 只选择需要的字段
    questions = query_db(
        'SELECT 问题ID, 提问用户ID, 问题内容, 发布日期, 回答数 FROM question ORDER BY 回答数 DESC',
        page=page,
        page_size=page_size
    )
    
    total = query_db('SELECT COUNT(*) as count FROM question', one=True)['count']
    total_pages = (total + page_size - 1) // page_size
    
    return render_template('question_list.html', 
                         email=questions,
                         current_page=page,
                         total_pages=total_pages)

@app.route('/question_check')
def question_check():
    """问题详情检查页面
    
    Returns:
        str: 返回问题详情页面的HTML内容
    """
    questions = query_db('SELECT * FROM question')
    return render_template('question_check.html', email=questions)

@app.route('/back_question', methods=['POST', 'GET'])
def back_question():
    """返回问题列表页面
    
    Returns:
        str: 返回问题列表页面的HTML内容
    """
    questions = query_db('SELECT * FROM question ORDER BY 回答数 DESC')
    return render_template('question_list.html', email=questions)

@app.route('/insert_question', methods=['POST', 'GET'])
def insert_question():
    """显示问题创建表单页面
    
    Returns:
        str: 返回问题创建表单页面的HTML内容
    """
    return render_template('question_add.html')

@app.route('/question_insert', methods=['POST'])
@login_required
def question_insert():
    """处理问题创建请求
    
    Returns:
        Response: 创建成功后重定向到问题列表页面
    """
    question_id = request.form.get('问题ID')
    question_content = request.form.get('问题内容')
    user_id = session.get('user_id')
    
    insert_db('INSERT INTO question (问题ID, 问题内容, 用户ID, 回答数) VALUES (%s, %s, %s, %s)',
              [question_id, question_content, user_id, 0])
    
    return redirect(url_for('question'))

@app.route('/delete_question', methods=['POST'])
@login_required
def delete_question():
    """处理问题删除请求
    
    Returns:
        str: 返回创作中心页面的HTML内容
    """
    question_id = request.form.get('问题ID')
    delete_db('DELETE FROM question WHERE 问题ID = %s', [question_id])
    
    questions = query_db('SELECT * FROM question WHERE 用户ID = %s', [session.get('user_id')])
    answers = query_db('SELECT * FROM answer WHERE 用户ID = %s', [session.get('user_id')])
    essays = query_db('SELECT * FROM essay WHERE 用户ID = %s', [session.get('user_id')])
    
    return render_template('create_center.html', questions=questions, answers=answers, essays=essays)

@app.route('/answer')
def answer():
    """显示所有回答列表
    
    Returns:
        str: 返回回答列表页面的HTML内容
    """
    answers = query_db('SELECT * FROM answer')
    return render_template('answer_list.html', email=answers)

@app.route('/insert_answer', methods=['POST', 'GET'])
def insert_answer():
    """显示回答创建表单页面
    
    Returns:
        str: 返回回答创建表单页面的HTML内容
    """
    return render_template('answer_insert.html')

@app.route('/read_answer', methods=['POST', 'GET'])
def read_answer():
    """处理回答查看请求
    
    Returns:
        str: 返回问题详情或回答列表页面的HTML内容
    """
    question_id = request.form.get('问题ID')
    if question_id:
        answers = query_db('SELECT * FROM answer WHERE 问题ID = %s', [question_id])
        return render_template('answer_list.html', email=answers)
    return redirect(url_for('question'))

@app.route('/answer_add', methods=['POST'])
@login_required
def answer_add():
    """处理添加回答请求
    
    Returns:
        str: 返回回答列表页面的HTML内容
    """
    answer_id = request.form.get('回答ID')
    answer_content = request.form.get('回答内容')
    question_id = request.form.get('问题ID')
    user_id = session.get('user_id')
    
    insert_db('INSERT INTO answer (回答ID, 回答内容, 问题ID, 用户ID) VALUES (%s, %s, %s, %s)',
              [answer_id, answer_content, question_id, user_id])
    
    update_db('UPDATE question SET 回答数 = 回答数 + 1 WHERE 问题ID = %s', [question_id])
    
    answers = query_db('SELECT * FROM answer')
    return render_template('answer_list.html', email=answers)

@app.route('/delete_answer', methods=['POST'])
@login_required
def delete_answer():
    """处理删除回答请求
    
    Returns:
        str: 返回创作中心页面的HTML内容
    """
    answer_id = request.form.get('回答ID')
    question_id = request.form.get('问题ID')
    
    delete_db('DELETE FROM answer WHERE 回答ID = %s', [answer_id])
    update_db('UPDATE question SET 回答数 = 回答数 - 1 WHERE 问题ID = %s', [question_id])
    
    questions = query_db('SELECT * FROM question WHERE 用户ID = %s', [session.get('user_id')])
    answers = query_db('SELECT * FROM answer WHERE 用户ID = %s', [session.get('user_id')])
    essays = query_db('SELECT * FROM essay WHERE 用户ID = %s', [session.get('user_id')])
    
    return render_template('create_center.html', questions=questions, answers=answers, essays=essays)

@app.route('/essay', methods=['POST', 'GET'])
def essay():
    """显示文章列表页面
    
    Returns:
        str: 返回文章列表页面的HTML内容，包含按赞同数降序排列的文章列表
    """
    page = request.args.get('page', 1, type=int)
    page_size = 10  # 每页显示10条记录
    
    # 只选择需要的字段
    essays = query_db(
        'SELECT 文章ID, 文章用户ID, 文章标题, 文章内容, 赞同数 FROM essay ORDER BY 赞同数 DESC',
        page=page,
        page_size=page_size
    )
    
    # 获取总记录数
    total = query_db('SELECT COUNT(*) as count FROM essay', one=True)['count']
    total_pages = (total + page_size - 1) // page_size
    
    return render_template('essay_list.html', 
                         email=essays, 
                         current_page=page,
                         total_pages=total_pages)

@app.route('/passage')
def passage():
    """显示文章列表页面的另一个路由
    
    Returns:
        str: 返回文章列表页面的HTML内容
    """
    essays = query_db('SELECT * FROM essay ORDER BY 赞同数 DESC')
    return render_template('essay_list.html', email=essays)

@app.route('/insert_essay', methods=['POST', 'GET'])
def insert_essay():
    """显示文章创建表单页面
    
    Returns:
        str: 返回文章创建表单页面的HTML内容
    """
    return render_template('essay_insert.html')

@app.route('/find_essay', methods=['POST'])
def find_essay():
    """处理文章搜索请求
    
    Returns:
        str: 返回符合条件的文章列表页面的HTML内容
    """
    essay_content = request.form.get('文章内容')
    essays = query_db('SELECT * FROM essay WHERE 文章内容 LIKE %s', [f'%{essay_content}%'])
    return render_template('essay_list.html', email=essays)

@app.route('/agree', methods=['POST'])
def agree():
    """处理文章点赞请求
    
    Returns:
        str: 返回更新后的文章列表页面的HTML内容
    """
    essay_id = request.form.get('文章ID')
    update_db('UPDATE essay SET 赞同数 = 赞同数 + 1 WHERE 文章ID = %s', [essay_id])
    
    essays = query_db('SELECT * FROM essay ORDER BY 赞同数 DESC')
    return render_template('essay_list.html', email=essays)

@app.route('/essay_add', methods=['POST'])
@login_required
def essay_add():
    """处理添加文章请求
    
    Returns:
        str: 返回文章列表页面的HTML内容
    """
    essay_id = request.form.get('文章ID')
    essay_content = request.form.get('文章内容')
    user_id = session.get('user_id')
    
    insert_db('INSERT INTO essay (文章ID, 文章内容, 用户ID, 赞同数) VALUES (%s, %s, %s, %s)',
              [essay_id, essay_content, user_id, 0])
    
    essays = query_db('SELECT * FROM essay ORDER BY 赞同数 DESC')
    return render_template('essay_list.html', email=essays)

@app.route('/delete_essay', methods=['POST'])
@login_required
def delete_essay():
    """处理删除文章请求
    
    Returns:
        str: 返回创作中心页面的HTML内容
    """
    essay_id = request.form.get('文章ID')
    delete_db('DELETE FROM essay WHERE 文章ID = %s', [essay_id])
    
    questions = query_db('SELECT * FROM question WHERE 用户ID = %s', [session.get('user_id')])
    answers = query_db('SELECT * FROM answer WHERE 用户ID = %s', [session.get('user_id')])
    essays = query_db('SELECT * FROM essay WHERE 用户ID = %s', [session.get('user_id')])
    
    return render_template('create_center.html', questions=questions, answers=answers, essays=essays)

@app.route('/ebook', methods=['POST', 'GET'])
def ebook():
    """显示电子书列表页面
    
    Returns:
        str: 返回电子书列表页面的HTML内容
    """
    ebooks = query_db('SELECT * FROM ebook')
    return render_template('ebook_shop.html', email=ebooks)

@app.route('/ebook_shop')
def ebook_shop():
    """显示电子书商店页面
    
    Returns:
        str: 返回电子书商店页面的HTML内容
    """
    ebooks = query_db('SELECT * FROM ebook')
    return render_template('ebook_shop.html', email=ebooks)

@app.route('/create', methods=['POST', 'GET'])
@login_required
def create():
    """显示创作中心页面
    
    Returns:
        str: 返回创作中心页面的HTML内容，根据用户权限显示不同内容
    """
    user_id = session.get('user_id')
    
    # 只选择需要的字段
    questions = query_db(
        'SELECT 问题ID, 提问用户ID, 问题内容, 发布日期, 回答数 FROM question WHERE 提问用户ID = %s',
        [user_id]
    )
    answers = query_db(
        'SELECT 回答ID, 问题ID, 用户ID, 回答文本 FROM answer WHERE 用户ID = %s',
        [user_id]
    )
    essays = query_db(
        'SELECT 文章ID, 文章用户ID, 文章标题, 文章内容, 赞同数 FROM essay WHERE 文章用户ID = %s',
        [user_id]
    )
    
    return render_template('create_center.html', questions=questions, answers=answers, essays=essays)

@app.route('/create_center')
@login_required
def create_center():
    """创作中心入口路由
    
    Returns:
        Response: 重定向到创作中心页面
    """
    return redirect(url_for('create'))

@app.route('/center_agree', methods=['POST'])
@login_required
def center_agree():
    """处理创作中心内的文章点赞请求
    
    Returns:
        str: 返回更新后的创作中心页面的HTML内容
    """
    essay_id = request.form.get('文章ID')
    update_db('UPDATE essay SET 赞同数 = 赞同数 + 1 WHERE 文章ID = %s', [essay_id])
    
    user_id = session.get('user_id')
    questions = query_db('SELECT * FROM question WHERE 用户ID = %s', [user_id])
    answers = query_db('SELECT * FROM answer WHERE 用户ID = %s', [user_id])
    essays = query_db('SELECT * FROM essay WHERE 用户ID = %s', [user_id])
    
    return render_template('create_center.html', questions=questions, answers=answers, essays=essays)

@app.route('/index1')
def user_add_page():
    """显示用户添加页面
    
    Returns:
        str: 返回用户添加页面的HTML内容
    """
    return render_template('user_add.html')

@app.route('/index2')
def user_delete_page():
    """显示用户删除页面
    
    Returns:
        str: 返回用户删除页面的HTML内容
    """
    return render_template('user_delete.html')

@app.route('/index3')
def user_edit_page():
    """显示用户编辑页面
    
    Returns:
        str: 返回用户编辑页面的HTML内容
    """
    return render_template('user_edit.html')

@app.route('/index4')
def user_search_page():
    """显示用户查询页面
    
    Returns:
        str: 返回用户查询页面的HTML内容
    """
    return render_template('user_search.html')

@app.route('/index5')
def user_display_page():
    """显示用户信息页面
    
    Returns:
        str: 返回用户信息页面的HTML内容，包含所有用户信息
    """
    users = query_db('SELECT * FROM user')
    return render_template('user_display.html', email=users)

@app.route('/turn_add', methods=['POST', 'GET'])
def turn_add():
    """转到用户添加页面
    
    Returns:
        Response: 重定向到用户添加页面
    """
    return redirect(url_for('user_add_page'))

@app.route('/turn_delete', methods=['POST', 'GET'])
def turn_delete():
    """转到用户删除页面
    
    Returns:
        Response: 重定向到用户删除页面
    """
    return redirect(url_for('user_delete_page'))

@app.route('/turn_change', methods=['POST', 'GET'])
def turn_change():
    """转到用户修改页面
    
    Returns:
        Response: 重定向到用户修改页面
    """
    return redirect(url_for('user_edit_page'))

@app.route('/turn_select', methods=['POST', 'GET'])
def turn_select():
    """转到用户查询页面
    
    Returns:
        Response: 重定向到用户查询页面
    """
    return redirect(url_for('user_search_page'))

@app.route('/add', methods=['POST'])
def add():
    """处理添加用户请求
    
    Returns:
        Response: 添加成功后重定向到首页
    """
    user_id = request.form.get('用户ID')
    user_name = request.form.get('用户名')
    
    insert_db('INSERT INTO user (用户ID, 用户名) VALUES (%s, %s)', [user_id, user_name])
    
    return redirect(url_for('index'))

@app.route('/delete', methods=['POST'])
@login_required
def delete():
    """处理删除用户请求
    
    Returns:
        str: 删除成功后返回登录页面
    """
    user_id = request.form.get('用户ID')
    delete_db('DELETE FROM user WHERE 用户ID = %s', [user_id])
    
    return render_template('login.html')

@app.route('/change', methods=['POST'])
@login_required
def change():
    """处理修改用户信息请求
    
    Returns:
        Response: 修改成功后重定向到首页
    """
    user_id = request.form.get('用户ID')
    user_name = request.form.get('用户名')
    
    update_db('UPDATE user SET 用户名 = %s WHERE 用户ID = %s', [user_name, user_id])
    
    return redirect(url_for('index'))

@app.route('/select', methods=['POST'])
def select():
    """处理查询用户信息请求
    
    Returns:
        str: 返回用户信息页面的HTML内容
    """
    user_id = request.form.get('用户ID')
    users = query_db('SELECT * FROM user WHERE 用户ID = %s', [user_id])
    return render_template('user_display.html', email=users)

@app.route('/returnback', methods=['POST'])
def returnback():
    """返回登录页面
    
    Returns:
        Response: 重定向到登录页面
    """
    return redirect(url_for('index'))

# 启动服务器
if __name__ == '__main__':
    # 在本地主机的8080端口运行应用，启用调试模式
    app.run(host='127.0.0.1', port=8080, debug=True) 