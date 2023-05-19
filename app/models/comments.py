from app import db

class Comment(db.Model):
    comment_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    comment_text = db.Column(db.String)
    timestamp = db.Column(db.DateTime, nullable=False) # default = datetime.now
    message = db.Column(db.string, nullable=False)
    user_id = db.Colum(db.Integer, db.ForeignKey("user.user_id"))
    board_id = db.Column(db.Intger, db.ForeignKey("board.board_id"))