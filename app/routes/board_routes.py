from flask import Blueprint, jsonify, request, make_response
from app import db
from app.models.boards import Board
from app.models.comments import Comment

board_bp = Blueprint('board', __name__, url_prefix = '/boards')

@board_bp.route("", methods = ['GET'])
def get_all_boards():

    boards = Board.query.all()
    boards_response = []

    for board in boards:
        boards_response.append(
            {
                'board_id' : board.board_id,
                'board_title' : board.board_title,
                'looking_for' : board.looking_for,
                'timestamp' : board.timestamp,
                'message' : board.message
            }
        )
    
    return jsonify(boards_response)

@board_bp.route("/<board_id>", methods = ['GET'])
def get_one_board(board_id):
    one_board = Board.query.get(board_id)
    one_board_response = {"Board": one_board.to_dict() }
    return jsonify(one_board_response),200

@board_bp.route("", methods = ['POST'])
def create_board():
    request_body = request.get_json()

    new_board = Board(
        board_title=request_body['board_title'],
        looking_for=request_body['looking_for'],
        timestamp=request_body['timestamp'],
        message=request_body['message']
    )
    response = {"Board": new_board.to_dict()}

    db.session.add(new_board)
    db.session.commit()

    return make_response(jsonify(response), 201)

@board_bp.route("/<board_id>", methods = ['DELETE'])
def delete_board(board_id):
    board = Board.query.get(board_id)

    db.session.delete(board)
    db.session.commit()

    return {"board_deleted": board.to_dict()}

@board_bp.route("/<board_id>", methods = ['PATCH'])
def update_board(board_id):
    board = Board.query.get(board_id)

    if not board:
        return make_response(jsonify({"error": "Board not found"}), 404)

    request_body = request.get_json()

    # Update the board attributes if they are present in the request body
    if 'board_title' in request_body:
        board.board_title = request_body['board_title']
    if 'looking_for' in request_body:
        board.looking_for = request_body['looking_for']
    if 'timestamp' in request_body:
        board.timestamp = request_body['timestamp']
    if 'message' in request_body:
        board.message = request_body['message']

    db.session.commit()

    return jsonify({"Board": board.to_dict()})

################################################
#  create a new comment to a board by id
@board_bp.route("/<board_id>/comments", methods=["POST"])
def create_comment_to_board(board_id):   
    # board = validate_model(Board, board_id)
    # board = validate_board(board_id)
    
    board = Board.query.get(board_id)

    if not board:
        return {"error": "Board not found"}, 404

    request_body = request.get_json()
    try:
        # new_comment = Comment.from_dict(request_body)
        new_comment = Comment(
            message=request_body["message"],
            timestamp=request_body["timestamp"],
            board_id=board.board_id
        )
    except KeyError:
        return {"details": "Missing Data"}, 400
    
    db.session.add(new_comment)
    db.session.commit()

    return {
        "comment" : {
            "id": new_comment.comment_id,
            "message": new_comment.message,
            "timestamp": new_comment.timestamp,
            "board_id": new_comment.board_id
        }
    }, 201

# GET all comments by a specific board
@board_bp.route("<board_id>/comments", methods=["GET"])
def read_all_comments_by_board(board_id):
    # board = validate_model(Board, board_id)
    # board = validate_board(board_id)
    comments = Comment.query.filter_by(board_id=board_id).all()
    comments_response = []
    # comments_response = [comment.to_dict() for comment in board.comments]

    for comment in comments:
        comments_response.append(
            {
                "id": comment.comment_id,
                "message": comment.message,
                "timestamp": comment.timestamp,
                "board_id": comment.board_id
            }
        )
    return jsonify(comments_response)

@board_bp.route("/<board_id>/comments/<comment_id>", methods=['DELETE'])
def delete_comment(board_id, comment_id):
    comment = Comment.query.get(comment_id)

    if not comment:
        return {"error": "Comment not found"}, 404

    db.session.delete(comment)
    db.session.commit()

    return {"comment_deleted": comment.to_dict()}
