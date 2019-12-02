from flask import Flask, render_template
import pymysql

# import os
# import sys
# from sqlalchemy import Column, ForeignKey, Integer, String
# from sqlalchemy.ext.declarative import declarative_base
# # from sqlalchemy.orm import relationship
# from sqlalchemy import create_engine

# # from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker

# engine = create_engine('mysql+pymysql://ps3:pword@localhost:3306/weather_station')

# Base = declarative_base()
app = Flask(__name__)

# class Station(Base):
#     __tablename__ = 'station'
#     sid = Column(Integer, primary_key=True)
#     scity = Column(String(100), nullable=True)
#     sstate = Column(String(100), nullable=True)
#     slatitude = Column(String, nullable=True)
#     slongitude = Column(String, nullable=True)


@app.route('/', methods=['GET', 'POST'])
def showInfo():
    db = pymysql.connect('localhost', 'ps3', 'pword', 'weather_station')
    cursor = db.cursor()
    sql = 'SELECT * FROM station;'
    try: 
        cursor.execute(sql)
        results = cursor.fetchall()
        return render_template('index.html', stations=results)
    except:
        print('Error fetching data')
    db.close()
    
#     DBSession = sessionmaker(bind=engine)
#     session = DBSession()
#     info = session.query(Station).all()
#     session.close()
#     

# def index():
#     return render_template('index.html')





if __name__ == '__main__':
    app.secret_key = 'cloud smile'
    app.debug = True
    app.run()