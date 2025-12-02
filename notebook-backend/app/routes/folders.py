from flask import Blueprint, request, jsonify
from .. import db
from ..models import Folder, Image
from ..utils.file_service import allowed_file, save_uploaded_file
import os

bp = Blueprint("folders", __name__)

def ensure_folder(date_str):
    f = Folder.query.filter_by(date=date_str).first()
    if not f:
        f = Folder(date=date_str, notes_html=None, notes_images=[])
        db.session.add(f)
        db.session.commit()
    return f

@bp.route("", methods=["GET"])
def list_folders():
    folders = Folder.query.order_by(Folder.date.desc()).all()
    return jsonify([f.to_dict() for f in folders]), 200

@bp.route("/<date_str>", methods=["GET"])
def get_folder(date_str):
    folder = Folder.query.filter_by(date=date_str).first()
    if not folder:
        return jsonify({"message": "folder not found"}), 404
    images = [img.to_dict() for img in folder.images]
    res = folder.to_dict()
    res["images"] = images
    return jsonify(res), 200

@bp.route("/<date_str>/notes", methods=["PUT", "POST"])
def update_notes(date_str):
    data = request.get_json() or {}
    html = data.get("notes_html")
    if html is None:
        return jsonify({"message": "notes_html is required"}), 400
    folder = ensure_folder(date_str)
    folder.notes_html = html
    db.session.commit()
    return jsonify(folder.to_dict()), 200

@bp.route("/<date_str>/notes/images", methods=["POST"])
def upload_note_images(date_str):
    folder = ensure_folder(date_str)
    if "file" not in request.files:
        return jsonify({"message": "file field required"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"message": "no selected file"}), 400
    if not allowed_file(file.filename):
        return jsonify({"message": "file type not allowed"}), 400

    saved_name, saved_path, url_path = save_uploaded_file(file, os.path.join("notes", date_str))
    images_list = folder.notes_images or []
    images_list.append(url_path)
    folder.notes_images = images_list
    db.session.commit()
    return jsonify({"url": url_path}), 201

