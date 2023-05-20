from app import db

class Neighbor(db.Model):
    neighbor_id  = db.Column(db.Integer, autoincrement = True, primary_key = True)
    name = db.Column(db.String)
    password = db.Column(db.String)
    zipcode = db.Column(db.Integer)
    email = db.Column(db.String)
    phone = db.Column(db.String)
    looking_to_trade = db.Column(db.Boolean)
    services = db.Column(db.ARRAY(db.String))
    skills = db.Column(db.ARRAY(db.String))
    # relationship with boards
    board = db.relationship("Board", backref="neighbor", lazy=True)
    # relationship with comments
    comment = db.relationship("Comment", backref="neighbor", lazy=True)
