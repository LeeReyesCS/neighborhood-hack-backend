from app import db

class Board(db.Model):
    board_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    board_title = db.Column(db.String)
    looking_for = db.Column(db.ARRAY(db.String))
    timestamp = db.Column(db.DateTime, nullable=False) # default = datetime.now
    message = db.Column(db.String, nullable=False)
    neighbor_id = db.Column(db.Integer, db.ForeignKey("neighbor.neighbor_id"))
    # relationship with comments
    comments = db.relationship("Comments", backref="boards", lazy=True) 