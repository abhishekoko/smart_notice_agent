# backend/routes/notice_routes.py
from flask import Blueprint, request, jsonify
from backend.models.notice_model import create_notice, get_all_notices, delete_notice, mark_notice_completed
from backend.utils.summarizer import TransformerSummarizer

notice_bp = Blueprint("notice_bp", __name__)
summarizer = TransformerSummarizer()

@notice_bp.route("/", methods=["POST"])
def create_notice_route():
    try:
        data = request.get_json()
        if not data or "title" not in data or "description" not in data:
            return jsonify({"error": "Missing title or description"}), 400

        # Summarize before saving
        if data.get("description"):
            data["description"] = summarizer.summarize(data["description"])

        notice_id = create_notice(data)
        return jsonify({"message": "Notice created successfully", "id": str(notice_id)}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@notice_bp.route("/", methods=["GET"])
def get_notices():
    try:
        user_id = request.args.get("user_id")
        notices = get_all_notices(user_id)
        return jsonify(notices), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@notice_bp.route("/<notice_id>", methods=["DELETE"])
def delete_notice_route(notice_id):
    try:
        deleted = delete_notice(notice_id)
        if deleted:
            return jsonify({"message": "Notice deleted"}), 200
        return jsonify({"error": "Notice not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@notice_bp.route("/<notice_id>/complete", methods=["PUT"])
def complete_notice_route(notice_id):
    try:
        modified = mark_notice_completed(notice_id)
        if modified:
            return jsonify({"message": "Notice marked as completed"}), 200
        return jsonify({"error": "Notice not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
