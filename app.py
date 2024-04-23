from flask import Flask, request, render_template, redirect, session, url_for, render_template_string
import pyodbc
import hashlib

app = Flask(__name__)
app.secret_key = 'your_super_secret_key'  # 设置一个安全的密钥

# 数据库连接
conn_str = (
    r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
    r'DBQ=./mydatabase.accdb;'
)
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# 首页
@app.route('/')
def index():
    cursor.execute("SELECT * FROM Products")
    products = cursor.fetchall()
    return render_template('index.html', products=products)

# 注册页
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        # hashed_password = hashlib.sha256(password.encode()).hexdigest()  # 密码哈希处理
        cursor.execute("INSERT INTO Users (Username, Password, Email) VALUES (?, ?, ?)", (username, password, email))
        conn.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

# 登录页
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # 构建 SQL 查询语句并插入用户提供的变量
        query = "SELECT * FROM Users WHERE Username = '" + username + "' AND Password = '" + password + "'"
        # 执行查询
        cursor.execute(query)
        # cursor.execute("SELECT * FROM Users WHERE Username = ? AND Password = ?", (username, password))
        user = cursor.fetchone()

        if user:
            session['user_id'] = user[0]  
            session['username'] = user[1]  # 新增：将用户名存入session
            if user[4]:  
                session['is_admin'] = True  
                return redirect(url_for('admin'))  
            else:
                return redirect(url_for('index'))  # 修改这里，用户登录后跳回首页而不是个人主页
        else:
            return "登录失败，请检查用户名和密码！"
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)  # 移除用户名
    session.pop('is_admin', None)
    return redirect(url_for('index'))

@app.route('/search')
def search():
    query = request.args.get('query')  # 获取搜索关键字
    query = '%' + query + '%'  # 添加通配符
    cursor.execute("SELECT * FROM Products WHERE ProductName LIKE '" + query + "'")
    search_results = cursor.fetchall()
    return render_template('search_results.html', results=search_results, query=query)

# 管理员界面
@app.route('/admin')
def admin():
    if 'user_id' not in session or not session.get('is_admin', False):
        return redirect(url_for('login'))  # 如果用户不是管理员，重定向到登录页面
    cursor.execute("SELECT * FROM Users")
    users = cursor.fetchall()
    cursor.execute("SELECT * FROM Products")
    products = cursor.fetchall()
    return render_template('admin.html', users=users, products=products)

# 删除用户
@app.route('/delete_user/<int:user_id>')
def delete_user(user_id):
    if 'user_id' not in session or not session.get('is_admin', False):
        return redirect(url_for('login'))  # 如果用户不是管理员，重定向到登录页面
    cursor.execute("DELETE FROM Users WHERE UserID = ?", (user_id,))
    conn.commit()
    return redirect(url_for('admin'))

# 删除产品
@app.route('/delete_product/<int:product_id>')
def delete_product(product_id):
    if 'user_id' not in session or not session.get('is_admin', False):
        return redirect(url_for('login'))  # 如果用户不是管理员，重定向到登录页面
    cursor.execute("DELETE FROM Products WHERE ProductID = ?", (product_id,))
    conn.commit()
    return redirect(url_for('admin'))

# 添加产品
@app.route('/add_product', methods=['POST'])
def add_product():
    if 'username' not in session or not session.get('is_admin', False):
        return redirect(url_for('login'))  # 如果用户不是管理员，重定向到登录页面
    product_name = request.form['product_name']
    product_price = request.form['product_price']
    product_category = request.form['product_category']
    cursor.execute("INSERT INTO Products (ProductName, Price, Category) VALUES (?, ?, ?)", (product_name, product_price, product_category))
    conn.commit()
    return redirect(url_for('admin'))

# 商品详情页
@app.route('/product')
def product_detail():
    product_id = request.args.get('product_id')
    cursor.execute("SELECT * FROM Products WHERE ProductID = " + product_id)
    product = cursor.fetchone()
    return render_template('product.html', product=product)


# 用户个人主页
@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))  
    user_id = session['user_id']
    cursor.execute("SELECT * FROM Users WHERE UserID = ?", (user_id,))
    user_info = cursor.fetchone()
    cursor.execute("SELECT * FROM Orders WHERE UserID = ?", (user_id,))
    orders = cursor.fetchall()
    return render_template('profile.html', user=user_info, orders=orders)

@app.route('/forget_password', methods=['GET', 'POST'])
def forget_password():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        new_password = request.form['newPassword']

        # 非参数化SQL查询
        try:
            # 首先验证用户是否存在
            user_query = f"SELECT UserID FROM Users WHERE Username = '{username}' AND Email = '{email}'"
            cursor.execute(user_query)
            user = cursor.fetchone()
            if user:
                # 如果用户存在，则更新其密码
                update_query = f"UPDATE Users SET Password = '{new_password}' WHERE Username = '{username}' AND Email = '{email}'"
                cursor.execute(update_query)
                conn.commit()
                return render_template('forget_password.html', title="密码已重置", message="密码已成功重置。", link="/login", link_text="登录")
            else:
                return render_template('forget_password.html', title="重置失败", message="未找到匹配的用户信息。", link="/forget_password", link_text="重试")
        except Exception as e:
            return render_template('forget_password.html', title="内部错误", message="内部错误，无法处理请求。", link="/forget_password", link_text="重试")
    else:
        return render_template('forget_password.html', title="重置密码")

if __name__ == '__main__':
    app.run(debug=True)
