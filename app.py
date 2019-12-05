from flask import Flask, render_template
import pymysql

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def showInfo():
    db = pymysql.connect('localhost', 'project', 'pword', 'projectdb')
    cursor = db.cursor()
    uid = 1;
    sql = 'SELECT * FROM Users WHERE uid = %d;' % uid
    try: 
        cursor.execute(sql)
        results = cursor.fetchall()
        return render_template('index.html', users=results)
    except:
        print('Error fetching data')
    db.close()
    

if __name__ == '__main__':
    app.secret_key = 'cloud smile'
    app.debug = True
    app.run()