from flask import Blueprint, jsonify, request
from services.blog_service import BlogService

blog_bp = Blueprint('blog_bp', __name__)
blog_service = BlogService()

@blog_bp.route('/similar_blogs/<int:blog_id>')
def find_similar_blogs(blog_id):
    similar_blogs = blog_service.find_similar_blogs(blog_id)
    # Convert list of Blog objects to list of dicts
    return jsonify([blog.to_dict() for blog in similar_blogs])

@blog_bp.route('/recent_blogs')
def get_recent_blogs():
    recent_blogs = blog_service.get_recent_blogs()
    # Convert list of Blog objects to list of dicts
    return jsonify([blog.to_dict() for blog in recent_blogs])

@blog_bp.route('/blog/<int:blog_id>')
def get_blog(blog_id):
    blog = blog_service.get_blog(blog_id)
    # Convert Blog object to dict
    return jsonify(blog.to_dict())

@blog_bp.post('/blog')
def create_blog():
    blog_data = request.json
    blog_service.create_blog(blog_data["content"], blog_data["title"], blog_data["author"], blog_data["categories"], blog_data["author_id"])
    return jsonify({"message": "Blog created successfully", "status": 200})

@blog_bp.put('/blog/<int:blog_id>')
def update_blog(blog_id):
    blog_data = request.json
    blog_service.update_blog(blog_id, blog_data["content"], blog_data["title"], blog_data["categories"])
    return jsonify({"message": "Blog updated successfully", "status": 200})

@blog_bp.delete('/blog/<int:blog_id>')
def delete_blog(blog_id):
    blog_service.delete_blog(blog_id)
    return jsonify({"message": "Blog deleted successfully", "status": 200})
