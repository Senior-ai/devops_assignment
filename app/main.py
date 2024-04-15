from flask import Flask, request, make_response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import socket

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/db_name'
# db = SQLAlchemy(app)

# class Counter(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     count = db.Column(db.Integer, default=0)

# class AccessLog(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     timestamp = db.Column(db.DateTime, default=datetime.utcnow)
#     client_ip = db.Column(db.String(15))
#     server_ip = db.Column(db.String(15))

@app.route('/')
def index():
    counter = Counter.query.first()
    if counter is None:
        counter = Counter(count=1)
        db.session.add(counter)
    else:
        counter.count += 1
    db.session.commit()

    response = make_response(socket.gethostbyname(socket.gethostname()))
    response.set_cookie('internal_ip', socket.gethostbyname(socket.gethostname()), max_age=timedelta(minutes=5))

    access_log = AccessLog(client_ip=request.remote_addr, server_ip=socket.gethostbyname(socket.gethostname()))
    db.session.add(access_log)
    db.session.commit()

    return response

@app.route('/showcount')
def show_count():
    counter = Counter.query.first()
    return str(counter.count) if counter else '0'

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
