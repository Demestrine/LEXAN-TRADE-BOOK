from flask import Blueprint, request, send_from_directory, abort
import os

bp = Blueprint("images", __name__)

@bp.route("/<folder>/<filename>", methods=["GET"])
def get_image(folder, filename):
    folder_path = os.path.join("uploads", folder)
    if not os.path.exists(os.path.join(folder_path, filename)):
        abort(404)
    return send_from_directory(folder_path, filename)
