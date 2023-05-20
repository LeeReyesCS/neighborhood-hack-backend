from flask import Blueprint, jsonify, request, make_response
from app import db
from app.models.comments import Comment

comment_bp = Blueprint('comment', __name__, url_prefix = '/comments')

# Post a comment
@comment_bp.route("", methods=["POST"])
def create_comment():
    request_body = request.get_json()
    
    try:
        new_comment = Comment(
            comment_id=request_body["comment_id"],
            message=request_body["message"],
            timestamp=request_body["timestamp"]
        )
    except KeyError:return {"details": "Missing Comment Descriptions"}, 400
    
    db.session.add(new_comment)
    db.session.commit()
    
    return {
        "comment": {
            "comment_id": new_comment.comment_id,
            "message": new_comment.message,
            "timestamp": new_comment.timestamp
        }
    }, 201
    
#Get all comments
@comment_bp.route("", methods = ['GET'])
def get_all_comments():

    comments = Comment.query.all()
    comments_response = []

    for words in comments:
        comments_response.append(
            {
            "comment_id": comment.comment_id,
            "message": comment.message,
            "timestamp": comment.timestamp
            }
        )

    return jsonify(comments_response)

# Get ONE comment
@comment_bp.route("/<comment_id>", methods=["GET"])
def read_one_comment(comment_id):
    comment = validate_comment(comment_id)

    return {
        "comment": {
            "comment_id": comment.comment_id,
            "timestamp": comment.timestamp,
            "message": comment.message
        }
    }
    
# Update a comment
@comment_bp.route("/<comment_id>", methods=["PUT"])
def update_comment(comment_id):
    comment = validate_comment(comment_id)

    request_body =request.get_json()
    comment.message = request_body["message"]

    comment.comment_id = int(comment.comment_id) 
    
    db.session.commit()
    
    return {
        "comment": {
            "comment_id": comment.comment_id,
            "message": comment.message,
            "timestampl": comment.timestamp
        }
    }

# Delete a comment
@comment_bp.route("/<comment_id>", methods=["DELETE"])
def delete_comment(comment_id):
    comment = validate_comment(comment_id)

    db.session.delete(comment)
    db.session.commit()


    return {
        "details": f'Comment {comment.comment_id} successfully deleted'
    }