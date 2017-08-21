# -*- coding: utf-8 -*-

import datetime
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.update(dict(
    # 主要是为了关闭一些不必要的提示
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    # 使用 sqlite 数据库
    SQLALCHEMY_DATABASE_URI='sqlite:////tmp/messages.db'
))
db = SQLAlchemy(app)


class Message(db.Model):
     # 在数据库中创建表时的表名称
    __tablename__ = 'message'

    id = db.Column(db.Integer, primary_key=True)
    # index 创建索引，nullable 表示不能为空
    name = db.Column(db.String(64), index=True, nullable=False)
    text = db.Column(db.String(1000), nullable=False)
    # 设置了 default 值，所以前端不需要传创建时间过来
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def to_dict(self):
        return {'name': self.name,
                'text': self.text,
                'created_at': self.created_at.strftime('%Y-%m-%dT%H:%M:%SZ')}


@app.route('/api/messages', methods=['GET'])
def get_messages():
    """获取所有 message, 按创建时间倒序排列"""
    messages = Message.query.order_by('created_at desc').all()
    return jsonify([message.to_dict() for message in messages])


@app.route('/api/messages', methods=['POST'])
def create_message():
    data = request.get_json()
    msg = Message(name=data['name'], text=data['text'])
    db.session.add(msg)
    db.session.commit()
    return jsonify(ok=True)


if __name__ == '__main__':
    app.run(debug=True)