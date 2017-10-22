from elrostick import db



class Outlets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20)) # name of the outlet will be used as part of the topic name
    channel = db.Column(db.String(8)) #channel in binary
    unit = db.Column(db.String(8)) #unit in binary
