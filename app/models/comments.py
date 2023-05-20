from app import db

class Comment(db.Model):
    comment_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    comment_text = db.Column(db.String)
    timestamp = db.Column(db.DateTime, nullable=False) # default = datetime.now
    message = db.Column(db.String, nullable=False)
    neighbor_id = db.Column(db.Integer, db.ForeignKey("neighbor.neighbor_id"))
    board_id = db.Column(db.Integer, db.ForeignKey("board.board_id"))