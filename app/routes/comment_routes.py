from flask import Blueprint, jsonify, request, make_response, abort
from app import db
from app.models.comments import Comment
from app.models.neighbors import Neighbor

comment_bp = Blueprint('comment', __name__, url_prefix = '/comments')

## Validate comment helper function
def validate_comment(comment_id):
    try:
        comment_id = int(comment_id)
    except:
        abort(make_response({"message": f"Comment {comment_id} invalid"}, 400))

    comment = Comment.query.get(comment_id)

    if not comment:
        abort(make_response({"message":f"Comment {comment_id} not found"}, 404))

    return comment

# Post a comment
@comment_bp.route("", methods=["POST"])
def create_comment():
    request_body = request.get_json()

    # Retrieve neighbor's name from the database based on the provided identifier
    neighbor_id = request_body.get("neighbor_id")  # Assuming you have a neighbor identifier in the request
    neighbor = Neighbor.query.get(neighbor_id)  # Assuming you have a Neighbor model and a query method

    if neighbor is None:
        return {"details": "Neighbor not found"}, 404

    try:
        new_comment = Comment(
            neighbor_id=neighbor.neighbor_id,
            message=request_body["message"],
            timestamp=request_body["timestamp"]
        )
    except KeyError:
        return {"details": "Missing Comment Descriptions"}, 400

    db.session.add(new_comment)
    db.session.commit()

    return {
        "comment": {
            "neighbor_id": new_comment.neighbor_id,
            "message": new_comment.message,
            "timestamp": new_comment.timestamp
        }
    }, 201
    
#Get all comments
@comment_bp.route("", methods = ['GET'])
def get_all_comments():

    comments = Comment.query.all()
    comments_response = []

    for comment in comments:
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