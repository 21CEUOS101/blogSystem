from models.blog_model import BlogModel

class BlogService:
    def __init__(self):
        self.blog_model = BlogModel()

    def find_similar_blogs(self, blog_id, n=5):
        return self.blog_model.find_similar_blogs(blog_id, n)

    def create_blog(self, content, title, author, categories, author_id):
        self.blog_model.create_blog(content, title, author, categories, author_id)

    def get_recent_blogs(self, n=5):
        return self.blog_model.get_recent_blogs(n)
    
    def get_blog(self, blog_id):
        return self.blog_model.get_blog(blog_id)
    
    def update_blog(self, blog_id, content, title, categories):
        self.blog_model.update_blog(blog_id, content, title, categories)

    def delete_blog(self, blog_id):
        self.blog_model.delete_blog(blog_id)


