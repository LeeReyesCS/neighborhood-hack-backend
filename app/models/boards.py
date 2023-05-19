from app import db

class Board(db.Model):
    board_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    board_title = db.Column(db.String)
    looking_for = db.Column(db.array(db.String))
    timestamp = db.Column(db.DateTime, nullable=False) # default = datetime.now
    message = db.Column(db.string, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"))
    # relationship with comments
    comments = db.relationship("Comments", backref="boards", lazy=True) 