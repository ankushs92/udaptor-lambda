from models import *
from udaptor import db


def create_tables():
    db.session.query(User).delete()
    db.create_all()
    db.session.commit()

    ankush = User(name="Ankush", email="ankush20058@gmail.com",
                  password="ankush")


    fernando = User(name="Fernando",
                    email="stefanini.mf@gmail.com",
                    password="fernando")

    pablo = User(name="Pablitos", email="e.pjlopez@gmail.com",
                  password="pablo")

    renecito = User(name="Renecito", email="renegomezlondono@gmail.com",
                  password="rene")

    yevgeniy = User(name="Yev", email="jonnypozdeev@gmail.com",
                  password="yev")

    db.session.add(ankush)
    db.session.add(fernando)
    db.session.add(pablo)
    db.session.add(renecito)
    db.session.add(yevgeniy)

    db.session.commit()
