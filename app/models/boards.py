from app import db
from app.models.comments import Comment
from app.models.neighbors import Neighbor

class Board(db.Model):
    board_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    board_title = db.Column(db.String)
    looking_for = db.Column(db.ARRAY(db.String))
    timestamp = db.Column(db.DateTime, nullable=False) # default = datetime.now
    message = db.Column(db.String, nullable=False)
    neighbor_id = db.Column(db.Integer, db.ForeignKey("neighbor.neighbor_id"))
    # relationship with comments
    comment = db.relationship("Comment", backref="board", lazy=True) 


    def to_dict(self):
        return {
            "board_id": self.board_id,
            "board_title": self.board_title,
            "looking_for": self.looking_for,
            "timestamp": self.timestamp,
            "message": self.message
        }