from models import *
import bcrypt
from udaptor import db

db.session.query(User).delete()
db.create_all()

db.session.commit()

ankush = User(name="Ankush", email="ankush20058@gmail.com",
              password=bcrypt.hashpw("ankush".encode("UTF-8"), bcrypt.gensalt(12)).decode())


fernando = User(name="Fernando",
                email="stefanini.mf@gmail.com",
                password=bcrypt.hashpw("fernando".encode("UTF-8"), bcrypt.gensalt(12)).decode())

pablo = User(name="Pablitos", email="e.pjlopez@gmail.com",
              password=bcrypt.hashpw("pablo".encode("UTF-8"), bcrypt.gensalt(12)).decode())

renecito = User(name="Renecito", email="renegomezlondono@gmail.com",
              password=bcrypt.hashpw("rene".encode("UTF-8"), bcrypt.gensalt(12)).decode())

yevgeniy = User(name="Yev", email="jonnypozdeev@gmail.com",
              password=bcrypt.hashpw("yev".encode("UTF-8"), bcrypt.gensalt(12)).decode())


db.session.add(ankush)
db.session.add(fernando)
db.session.add(pablo)
db.session.add(renecito)
db.session.add(yevgeniy)

db.session.commit()
