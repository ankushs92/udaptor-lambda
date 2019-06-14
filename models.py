from udaptor import db


class PossibleJobStates():
    STARTED = 1
    COMPLETED = 2
    FAILED = 3

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False) #Bcrypt

    def __str__(self):
        return "<User = {}>".format(self.email)



class Job(db.Model):
    __tablename__ = "jobs"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    input_vendor = db.Column(db.String(100), nullable=False)
    output_vendor = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.TIMESTAMP, nullable=False)
    state = db.Column(db.SmallInteger, nullable=False)
    file_url = db.Column(db.String(1000), nullable=False)

    def __str__(self):
        return "<JobState = Id: {}, User Id : {}, Input Vendor : {}, Output Vendor : {}>".format(self.email, self.user_id, self.input_vendor, self.output_vendor)
