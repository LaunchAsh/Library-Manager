from flask import jsonify
from flask import Blueprint, send_from_directory

bp = Blueprint('image', __name__)

@bp.route('/<path:filename>')
def serve_image(filename):
    root_dir = '../app/images'
    try:
        image = send_from_directory(root_dir, filename)
        return image or None , 200
    except FileNotFoundError:
        return jsonify({"message": "NOT FOUND"}), 404