#coding=utf-8

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from config import *
from datetime import datetime

app = Flask(__name__)
#db = SQLAlchemy()
cfg = Config()
app.config.from_object(cfg)
db = SQLAlchemy(app)
db.engine.echo = True;

class User(db.Model):
    """
    定义三个字段，表名为Model名小写
    """
    id = db.Column( db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    age = db.Column(db.Integer, index=True)


    def __init__(self, username, email, age):
        self.username = username
        self.email = email
        self.age = age;

    def __repr__(self):
        return '<User %r email:%r>' % (self.username, self.email)

    def save(self):
        db.session.add(self)
        db.session.commit()

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    body = db.Column(db.Text)
    pub_date = db.Column(db.DateTime)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category',
        backref=db.backref('posts', lazy='dynamic'))

    def __init__(self, title, body, category, pub_date=None):
        self.title = title
        self.body = body
        if pub_date is None:
            pub_date = datetime.utcnow()
        self.pub_date = pub_date
        self.category = category

    def __repr__(self):
        return '<Post %r>' % self.title


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category %r>' % self.name

db.create_all()
u = User("wanglaowu5", "12125@qq.com", 0)
try:
    u.save()
except Exception as e:
    db.session.rollback()
    print e

users = User.query.all()
for u in users:
    print u

uuu = User.query.filter_by(username=u'wanglaowu2').all()
print(uuu)

res = User.query.filter_by(username=u'wanglaowu2').update({
    User.age: User.age + 1
})

db.session.commit()


import time;

localtime = time.localtime(time.time())
print "Local current time :", localtime
localtime = time.asctime( time.localtime(time.time()) )
print "Local current time :", localtime

def utc2local(utc_st):
    """UTC时间转本地时间（+8:00）"""
    now_stamp = time.time()
    local_time = datetime.fromtimestamp(now_stamp)
    utc_time = datetime.utcfromtimestamp(now_stamp)
    offset = local_time - utc_time
    local_st = utc_st + offset
    return local_st

def local2utc(local_st):
    """本地时间转UTC时间（-8:00）"""
    time_struct = time.mktime(local_st.timetuple())
    utc_st = datetime.utcfromtimestamp(time_struct)
    return utc_st

utc_time = datetime(2014, 9, 18, 10, 42, 16, 126000)

# utc转本地
local_time = utc2local(utc_time)
print local_time.strftime("%Y-%m-%d %H:%M:%S")
# output：2014-09-18 18:42:16


# 本地转utc
utc_tran = local2utc(local_time)
print utc_tran.strftime("%Y-%m-%d %H:%M:%S")
# output：2014-09-18 10:42:16 