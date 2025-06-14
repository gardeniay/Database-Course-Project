import web  # 导入web.py框架
import datetime  # 导入日期时间模块，用于记录时间戳
import os  # 导入操作系统模块，用于获取环境变量
import sys

# 管理员ID列表，拥有特殊权限
manister=[1,3,7]

# webpy模块具备URL匹配功能
# URLs配置元组，格式为(URL路径, 处理类名称)
urls = (
   '/','index',  # 根路径，映射到index类，显示登录页面
   '/login', 'login',  # 登录处理
   '/shouye', 'home_page',  # 首页
   '/back_shouye', 'back_home',  # 返回首页
   
   # 问题部分 - 管理用户提问功能的路由
   '/ask','ask',  # 提问入口
   '/question','question',  # 问题列表页
   '/question_check','question_check',  # 问题检查
   '/insert_question','insert_question',  # 插入问题表单
   '/question_insert','question_insert',  # 执行问题插入
   '/delete_question','delete_question',  # 删除问题
   '/back_question','back_question',  # 返回问题列表
   
   # 回答部分 - 管理用户回答功能的路由
   '/insert_answer','insert_answer',  # 插入回答表单
   '/read_answer','read_answer',  # 阅读回答
   '/answer','answer',  # 回答列表
   '/answer_add','answer_add',  # 添加回答
   '/answer_insert','answer_insert',  # 执行回答插入
   '/delete_answer','delete_answer',  # 删除回答
   
   # 文章部分 - 管理文章功能的路由
   '/essay','essay',  # 文章入口
   '/passage','passage',  # 文章列表
   '/insert_essay','insert_essay',  # 插入文章表单
   '/find_essay','find_essay',  # 查找文章
   '/agree','agree',  # 赞同文章
   '/essay_insert','essay_insert',  # 执行文章插入
   '/essay_add','essay_add',  # 添加文章
   '/delete_essay','delete_essay',  # 删除文章
   
   # 电子书部分 - 电子书相关功能
   '/ebook','ebook',  # 电子书入口
   '/ebook_shop','ebook_shop',  # 电子书商店
   
   # 用户中心部分 - 用户账户管理
   '/user','user',  # 用户入口
   '/index','user_center',  # 用户主页
   '/index1', 'user_add_page',  # 添加用户页面
   '/index2', 'user_delete_page',  # 删除用户页面
   '/index3', 'user_edit_page',  # 修改用户页面
   '/index4', 'user_search_page',  # 查询用户页面
   '/index5', 'user_display_page',  # 用户信息显示
   '/add','add',  # 添加用户操作
   '/delete','delete',  # 删除用户操作
   '/change','change',  # 修改用户操作
   '/select','select',  # 查询用户操作
   '/turn_add','turn_add',  # 转向添加页面
   '/turn_change','turn_change',  # 转向修改页面
   '/turn_delete','turn_delete',  # 转向删除页面
   '/turn_select','turn_select',  # 转向查询页面
   '/returnback','returnback',  # 返回
   
   # 创作中心部分 - 用户创作内容管理
   '/create','create',  # 创作中心入口
   '/create_center','create_center',  # 创作中心主页，显示用户的所有创作
   '/center_agree','center_agree',  # 创作中心文章点赞
)

# 全局变量，用于存储当前登录的用户ID和被查看的问题ID
user_ID=0
question_ID=0

# 确定程序目录，创建web应用实例
app = web.application(urls, globals())
# 配置模板目录
render = web.template.render('templates/')

# 从环境变量获取数据库配置，如果不存在则使用默认值
db_host = os.getenv('DB_HOST', '127.0.0.1')  # 数据库主机
db_port = int(os.getenv('DB_PORT', '3306'))  # MySQL默认端口是3306
db_name = os.getenv('DB_NAME', 'zhihu')  # 数据库名称
db_user = os.getenv('DB_USER', 'root')  # 数据库用户名
db_password = os.getenv('DB_PASSWORD', '928520zjf.')  # 数据库密码

# 创建数据库连接
db = web.database(dbn='mysql',  # 数据库类型
                 host=db_host,  # 主机
                 port=db_port,  # 端口
                 db=db_name,    # 数据库名
                 user=db_user,  # 用户名
                 pw=db_password)  # 密码

# ==================== 表示层(View) ====================

# 登录页面处理类
class index:
    def GET(self):
        # 返回登录页面
        return render.login()

# 首页处理类
class home_page:
    def GET(self):
        # 返回首页
        return render.shouye()

# ==================== 业务逻辑层(Controller) ====================

# 提问处理类
class ask:
    def POST(self):
        # 重定向到问题页面
        raise web.seeother('/question')   
        
    def GET(self):
        # GET请求也重定向到问题页面
        raise web.seeother('/question')

# 返回问题列表处理类
class back_question:
    def POST(self):
        # 查询问题表并按回答数降序排序
        email = db.query('select * from question order by 回答数 DESC')
        # 返回问题列表页面，并传递问题数据
        return render.question_list(email)
        
    def GET(self):
        # 查询问题表并按回答数降序排序
        email = db.query('select * from question order by 回答数 DESC')
        # 返回问题列表页面，并传递问题数据
        return render.question_list(email)

# 返回首页处理类
class back_home:
    def POST(self):
        # 返回首页
        return render.shouye()
        
    def GET(self):
        # 返回首页
        return render.shouye()

# 用户处理类
class user:
    def POST(self):
        # 重定向到用户主页
        raise web.seeother('/index')
        
    def GET(self):
        # GET请求也重定向到用户主页
        raise web.seeother('/index')

# 电子书处理类
class ebook:
    def POST(self):
        # 查询电子书表
        email = db.query('select * from ebook')
        # 返回电子书商店页面，并传递电子书数据
        return render.ebook_shop(email) 
        
    def GET(self):
        # 查询电子书表
        email = db.query('select * from ebook')
        # 返回电子书商店页面，并传递电子书数据
        return render.ebook_shop(email)

# 文章处理类
class essay:
    def POST(self):
        # 查询文章表并按赞同数降序排序
        email=db.query('select * from essay order by 赞同数 DESC')
        # 返回文章列表页面，并传递文章数据
        return render.essay_list(email) 
        
    def GET(self):
        # 查询文章表并按赞同数降序排序
        email=db.query('select * from essay order by 赞同数 DESC')
        # 返回文章列表页面，并传递文章数据
        return render.essay_list(email)

# 文章处理类
class passage:
    def GET(self):
        # 查询文章表并按赞同数降序排序
        email=db.query('select * from essay order by 赞同数 DESC')
        # 返回文章列表页面，并传递文章数据
        return render.essay_list(email)

# 创作中心处理类
class create:
    def POST(self):
        # 根据用户权限显示不同内容
        if user_ID not in manister:
            # 非管理员用户只能看到自己的内容
            questions=db.query(f'select * from question where 提问用户ID={user_ID}')
            answers=db.query(f'select * from answer where 用户ID={user_ID}')
            essays=db.query(f'select * from essay where 文章用户ID={user_ID}')
            return render.create_center(questions,answers,essays)   
        else:
            # 管理员可以看到所有内容
            questions=db.query(f'select * from question')
            answers=db.query(f'select * from answer')
            essays=db.query(f'select * from essay')
            return render.create_center(questions,answers,essays)
            
    def GET(self):
        # 根据用户权限显示不同内容
        if user_ID not in manister:
            # 非管理员用户只能看到自己的内容
            questions=db.query(f'select * from question where 提问用户ID={user_ID}')
            answers=db.query(f'select * from answer where 用户ID={user_ID}')
            essays=db.query(f'select * from essay where 文章用户ID={user_ID}')
            return render.create_center(questions,answers,essays)   
        else:
            # 管理员可以看到所有内容
            questions=db.query(f'select * from question')
            answers=db.query(f'select * from answer')
            essays=db.query(f'select * from essay')
            return render.create_center(questions,answers,essays)

# 插入问题表单处理类
class insert_question:
    def POST(self):
        print("touch it\n")
        # 返回添加问题页面
        return render.question_add() 

# 插入回答表单处理类
class insert_answer:
    def POST(self):
        # 返回添加回答页面
        return render.answer_insert() 

# 插入文章表单处理类
class insert_essay:
    def POST(self):
        # 返回添加文章页面
        return render.essay_insert() 

# 转向添加用户页面处理类
class turn_add:
    def POST(self):
        print("touch it\n")
        # 重定向到添加用户页面
        raise web.seeother('/index1')

# 转向删除用户页面处理类
class turn_delete:
    def POST(self):
        print("touch it\n")
        # 重定向到删除用户页面
        raise web.seeother('/index2')

# 转向修改用户页面处理类
class turn_change:
    def POST(self):
        print("touch it\n")
        # 重定向到修改用户页面
        raise web.seeother('/index3')

# 转向查询用户页面处理类
class turn_select:
    def POST(self):
        print("touch it\n")
        # 重定向到查询用户页面
        raise web.seeother('/index4')

# 返回处理类
class returnback:
    def POST(self):
        # 重定向到首页
        raise web.seeother('/')

# ==================== 表示层(View) - GET方法 ====================

# 首页GET处理类(与上面POST方法的类同名，但处理不同的HTTP方法)
class shouye:
    def GET(self):
        # 返回首页
        return render.shouye()

# 问题列表处理类
class question:
    def GET(self):
        # 查询问题表并按回答数降序排序
        email = db.query('select * from question order by 回答数 DESC')
        # 返回问题列表页面，并传递问题数据
        return render.question_list(email)  

# 问题检查处理类
class question_check:
    def GET(self):
        # 查询问题表
        email = db.query('select * from question')
        # 返回问题检查页面，并传递问题数据
        return render.question_check(email) 

# 回答列表处理类
class answer:
    def GET(self):
        # 查询回答表
        email = db.query('select * from answer')
        # 返回回答列表页面，并传递回答数据
        return render.answer_list(email) 

# 用户主页处理类
class user_center:
    def GET(self):
        # 返回用户主页
        return render.user_center()
        
    def POST(self):
        # POST请求也返回用户主页
        return render.user_center()

# 添加用户页面处理类
class user_add_page:
    def GET(self):
        # 返回添加用户页面
        return render.user_add()

# 删除用户页面处理类
class user_delete_page:
    def GET(self):
        # 返回删除用户页面
        return render.user_delete()

# 修改用户页面处理类
class user_edit_page:
    def GET(self):
        # 返回修改用户页面
        return render.user_edit()

# 查询用户页面处理类
class user_search_page:
    def GET(self):
        # 返回查询用户页面
        return render.user_search()

# 用户信息显示页面处理类
class user_display_page:
    def GET(self):
        # 查询用户表
        email = db.query('select * from user')
        # 返回用户信息页面，并传递用户数据
        return render.user_display(email)

# ==================== 数据访问层(Model) ====================

# 添加用户处理类
class add:
    def POST(self):
        # 获取表单提交的数据
        i = web.input()
        print(i.用户ID)
        # 判断输入是否有效
        if i.用户ID!='用户ID' and i.用户名!='用户名' and i.个人简介!='个人简介' and i.所在行业!='所在行业':
            # 执行插入操作
            n = db.insert('user', 用户ID=i.用户ID, 用户名=i.用户名,个人简介=i.个人简介,所在行业=i.所在行业)
            # 重定向到首页，POST方法接收到一个post并完成处理后，它将给浏览器发送一个303消息和新网址
            raise web.seeother('/') 
        else:   
            # 如果输入无效，重定向到首页
            raise web.seeother('/')

# 删除用户处理类
class delete:
    def POST(self):
        # 获取表单提交的数据
        i = web.input()
        print(i)
        a=i.用户ID
        print(a)
        # 判断是否为当前用户
        if a!=user_ID:
            # 不能删除其他用户，返回首页
            return render.shouye()
        else:
            # 删除当前用户
            db.delete('user',where='用户ID = $a',vars=locals())
            # 返回登录页面
            return render.login()
        # 重定向到首页(注意：此代码不会执行，因为前面已经有return)
        raise web.seeother('/')

# 修改用户处理类
class change:
    def POST(self):
        # 获取表单提交的数据
        i=web.input()
        print(i)
        a=i.用户ID
        b=i.用户名
        # 如果用户名不为默认值，则更新
        if b!='用户名':
            db.update('user',where='用户ID=$a',vars=locals(), 用户名=i.用户名)
        c=i.个人简介
        # 如果个人简介不为默认值，则更新
        if c!='个人简介':
            db.update('user',where='用户ID=$a',vars=locals(), 个人简介=i.个人简介)
        d=i.所在行业
        # 如果所在行业不为默认值，则更新
        if d!='所在行业':
            db.update('user',where='用户ID=$a',vars=locals(), 所在行业=i.所在行业)
        # 重定向到首页
        raise web.seeother('/')

# 查询用户处理类
class select:
    def POST(self):
        # 获取表单提交的数据
        i=web.input()
        print(i)
        a=i.用户ID
        # 判断是查询所有用户还是特定用户
        if i.用户ID=='用户ID':
            # 查询所有用户
            information = db.select('user')
            print(information)
            return render.user_display(information)
        else:
            # 查询特定用户
            information = db.select('user',where='用户ID=$a',vars=locals())
            return render.user_display(information)

# 登录处理类
class login:
    def POST(self):
        i=web.input()
        print(i)
        flag=0
        yonghu=[]
        email=db.query(f"select 用户ID from user")
        for j in email:
            if int(i.用户ID)==j.用户ID:
                flag=1
                global user_ID
                user_ID=j.用户ID
                print(user_ID)
                return render.shouye()
                break
        if flag==0:
            return render.nologin()

# 阅读回答处理类
class read_answer:
    def POST(self):
        i=web.input()
        print(i)
        if i.get('问题内容')!=None:
            spring=i.问题内容
            email=db.query(f"select * from question where 问题内容 like '%{spring}%'")
            return render.question_check(email)  
        else:
            a=i.问题ID
            global question_ID
            question_ID=a
            email = db.query(f'select * from answer where 问题ID={a} order by 回答时间 DESC')
            return render.answer_list(email)  

# 插入问题处理类
class question_insert:
    def POST(self):
        q=web.input()
        print(q)
        num=[]
        email=db.query(f"select 问题ID from question")
        for i in email:
            num.append(i.问题ID)
        for j in range(1,1000):
            if j in num:
                continue
            else:
                wenti=j
                break
        print(wenti)
        nowtime=datetime.datetime.now().strftime('%Y-%m-%d')
        print(nowtime)
        if q.问题内容!='问题内容':
            n = db.insert('question', 问题ID=wenti, 提问用户ID=user_ID,问题内容=q.问题内容,发布日期=nowtime,回答数=0)
            email = db.query('select * from question order by 回答数 DESC')
            return render.question_list(email)

# 添加回答处理类
class answer_add:
    def POST(self):
        q=web.input()
        print(q)
        nowtime=datetime.datetime.now().strftime('%Y-%m-%d')
        num=[]
        email=db.query(f"select 回答ID from answer")
        for i in email:
            num.append(i.回答ID)
        for j in range(1,1000):
            if j in num:
                continue
            else:
                huida=j
                break
        print(huida)
        n = db.insert('answer', 回答ID=huida,问题ID=int(question_ID), 用户ID=int(user_ID),回答文本=q.回答文本,回答时间=nowtime)
        email = db.query(f'select * from answer where 问题ID={question_ID} order by 回答时间 DESC')
        return render.answer_list(email)  

# 查找文章处理类
class find_essay:
    def POST(self):
        q=web.input()
        print(q)
        if q.get('文章标题内容')==None and q.get('文章内容')==None:
            email=db.query('select * from essay')
            return render.essay_list(email)
        if q.get('文章标题内容')!=None and q.get('文章内容')==None:
            spring=q.文章标题内容
            email=db.query(f"select * from essay where 文章标题 like '%{spring}%'") 
            return render.essay_list(email)
        if q.get('文章标题内容')==None and q.get('文章内容')!=None:
            spring=q.文章内容
            email=db.query(f"select * from essay where 文章内容 like '%{spring}%'") 
            return render.essay_list(email) 
        if q.get('文章标题内容')!=None and q.get('文章内容')!=None:
            spring=q.文章内容
            email=db.query(f"select * from essay where 文章内容 like '%{spring}%' or 文章标题 like '%{spring}%'") 
            return render.essay_list(email) 

# 赞同文章处理类
class agree:
    def POST(self):
        q=web.input()
        print(q)
        a=q.文章ID
        n=db.query(f'update essay set 赞同数=赞同数+1 where 文章ID={a}')
        email=db.query("select * from essay") 
        return render.essay_list(email)    

# 创作中心赞同文章处理类
class center_agree:
    def POST(self):
        q=web.input()
        print(q)
        a=q.文章ID
        n=db.query(f'update essay set 赞同数=赞同数+1 where 文章ID={a}')
        questions=db.query(f'select * from question where 提问用户ID={user_ID}')
        answers=db.query(f'select * from answer where 用户ID={user_ID}')
        essays=db.query(f'select * from essay where 文章用户ID={user_ID}')
        return render.create_center(questions,answers,essays)     

# 添加文章处理类
class essay_add:
    def POST(self):
        q=web.input()
        print(q)
        nowtime=datetime.datetime.now().strftime('%Y-%m-%d')
        num=[]
        email=db.query(f"select 文章ID from essay")
        for i in email:
            num.append(i.文章ID)
        for j in range(1,1000):
            if j in num:
                continue
            else:
                wenzhang=j
                break
        print(wenzhang)
        if q.文章标题!='文章标题' and q.文章内容!='文章内容':
            n = db.insert('essay',文章ID=wenzhang ,文章用户ID=int(user_ID),文章标题=q.文章标题,文章内容=q.文章内容,发布时间=nowtime,赞同数=0)
            email=db.query("select * from essay") 
            return render.essay_list(email) 
        else:
             return render.shouye() 

# 删除问题处理类
class delete_question:
    def POST(self):
        q=web.input()
        n=db.query(f'delete from question where 问题ID={q.问题ID}')
        if user_ID not in manister:
            questions=db.query(f'select * from question where 提问用户ID={user_ID}')
            answers=db.query(f'select * from answer where 用户ID={user_ID}')
            essays=db.query(f'select * from essay where 文章用户ID={user_ID}')
            return render.create_center(questions,answers,essays)   
        else:
            questions=db.query(f'select * from question')
            answers=db.query(f'select * from answer')
            essays=db.query(f'select * from essay')
            return render.create_center(questions,answers,essays)  

# 删除回答处理类
class delete_answer:
    def POST(self):
        q=web.input()
        n=db.query(f'delete from answer where 回答ID={q.回答ID}')
        if user_ID not in manister:
            questions=db.query(f'select * from question where 提问用户ID={user_ID}')
            answers=db.query(f'select * from answer where 用户ID={user_ID}')
            essays=db.query(f'select * from essay where 文章用户ID={user_ID}')
            return render.create_center(questions,answers,essays)   
        else:
            questions=db.query(f'select * from question')
            answers=db.query(f'select * from answer')
            essays=db.query(f'select * from essay')
            return render.create_center(questions,answers,essays)  

# 删除文章处理类
class delete_essay:
    def POST(self):
        q=web.input()
        n=db.query(f'delete from essay where 文章ID={q.文章ID}')
        if user_ID not in manister:
            questions=db.query(f'select * from question where 提问用户ID={user_ID}')
            answers=db.query(f'select * from answer where 用户ID={user_ID}')
            essays=db.query(f'select * from essay where 文章用户ID={user_ID}')
            return render.create_center(questions,answers,essays)   
        else:
            questions=db.query(f'select * from question')
            answers=db.query(f'select * from answer')
            essays=db.query(f'select * from essay')
            return render.create_center(questions,answers,essays)        

if __name__ == "__main__":
    # 修改默认主机地址为127.0.0.1
    sys.argv = ['webto.py', '127.0.0.1:8080']
    app.run()