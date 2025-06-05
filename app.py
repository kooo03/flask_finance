from flask import Flask, render_template, redirect, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Record
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 添加调试信息
print("📡 SQLALCHEMY_DATABASE_URI =", os.environ.get("SQLALCHEMY_DATABASE_URI"))
assert os.environ.get("SQLALCHEMY_DATABASE_URI") is not None, "❌ SQLALCHEMY_DATABASE_URI 未设置，无法连接数据库！"

# 仅 init_app，不再创建新实例
db = SQLAlchemy(app)

with app.app_context():
    try:
        print("🔧 初始化数据库表中...")
        db.create_all()
        print("✅ 数据表创建完成")
    except Exception as e:
        print("❌ 数据表初始化失败:", e)


# 初始化登录管理器
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        if User.query.filter_by(username=username).first():
            flash("Username already exists.")
            return redirect(url_for('register'))
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash("Invalid credentials.")
    return render_template('login.html')

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if request.method == 'POST':
        record = Record(
            user_id=current_user.id,
            type=request.form['type'],
            amount=float(request.form['amount']),
            description=request.form['description']
        )
        db.session.add(record)
        db.session.commit()
    records = Record.query.filter_by(user_id=current_user.id).all()
    income = sum(r.amount for r in records if r.type == 'income')
    expense = sum(r.amount for r in records if r.type == 'expense')
    return render_template('dashboard.html', records=records, income=income, expense=expense)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# 自动创建数据库表
if __name__ == '__main__':
    with app.app_context():
        import time
        time.sleep(10)
        db.create_all()
    app.run(debug=True, host='0.0.0.0')  # 确保容器中可访问
