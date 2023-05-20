from flask import Blueprint, jsonify, request, make_response
from app import db
from app.models.boards import Board

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
    one_board_response = {"Board": order.to_dict() }
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