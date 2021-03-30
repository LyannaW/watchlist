from flask_sqlalchemy import SQLAlchemy
from flask import render_template
from flask import Flask,request
import os
import sys
import click


WIN = sys.platform.startswith('win')
if WIN: # 如果是 Windows 系统，使用三个斜线
    prefix = 'sqlite:///'
else: # 否则使用四个斜线
    prefix = 'sqlite:////'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # 关闭对模型修改的监控
# 在扩展类实例化前加载配置
db = SQLAlchemy(app) # 初始化扩展，传入程序实例app
@app.cli.command() # 注册为命令
@click.option('--drop', is_flag=True, help='Create after drop.')
    # 设置选项
def initdb(drop):
    """Initialize the database."""
    if drop: # 判断是否输入了选项
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.') # 输出提示信息

@app.route('/')
def hello():
    return render_template('index.html')


class User(db.Model): # 表名将会是 user（自动生成，小写处理）,（声明继承db.Model）
    id = db.Column(db.Integer, primary_key=True) # 主键
    name = db.Column(db.String(20)) # 名字


class Movie(db.Model): # 表名将会是 movie
    id = db.Column(db.Integer, primary_key=True) # 主键
    title = db.Column(db.String(60)) # 电影标题
    year = db.Column(db.String(4)) # 电影年份


if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True)