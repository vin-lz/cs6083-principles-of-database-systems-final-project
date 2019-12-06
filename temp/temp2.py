from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.orm import Session
# from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://project:pword@localhost:3306/projectdb'
db = SQLAlchemy(app)

Base = automap_base()
Base.prepare(db.engine, reflect=True)
User = Base.classes.Users

@app.route('/', methods=['GET', 'POST'])
def index():
    results = db.session.query(User).all()
    for r in results:
        print(r)
    return render_template('index.html', users=results)

if __name__ == '__main__':
    app.secret_key = 'cloud smile'

    app.debug = True
    app.run()