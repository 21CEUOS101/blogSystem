import json
from .db import get_db
from langchain_community.embeddings.ollama import OllamaEmbeddings
import uuid , datetime

class Blog:
    def __init__(self, blog_id, title, author, content, categories, date, author_id):
        self.blog_id = blog_id
        self.title = title
        self.author = author
        self.content = content
        self.categories = categories
        self.date = date
        self.author_id = author_id

    def to_dict(self):
        return {
            "blog_id": self.blog_id,
            "title": self.title,
            "author": self.author,
            "content": self.content,
            "categories": self.categories,
            "date": self.date,
            "author_id": self.author_id
        }

    @staticmethod
    def from_dict(data):
        return Blog(
            blog_id=data["blog_id"],
            title=data["title"],
            author=data["author"],
            content=data["content"],
            categories=data["categories"],
            date=data["date"],
            author_id=data["author_id"]
        )

    def __str__(self):
        return json.dumps(self.to_dict())

class BlogModel:
    def __init__(self):
        self.db = get_db()
        self.blogs = self.db.get_collection("blogs")
        self.blogs_embeddings = self.db.get_collection("blog_embeddings")

    def find_similar_blogs(self, blog_id, n=5):
        sample_blog = self.blogs_embeddings.find_one({"blog_id": blog_id})
        if sample_blog is None:
            print(f"No blog found with blog_id: {blog_id}")
            return []

        print(sample_blog["blog_id"])  # This line will work only if sample_blog is not None
        
        similar_blogs_id = self.blogs_embeddings.aggregate([
            {
                "$vectorSearch": {
                    "index": "vector_index",
                    "path": "embedding",
                    "queryVector": sample_blog["embedding"],
                    "numCandidates": 10,
                    "limit": n+1
                }
            },
            {
                "$project": {
                    "blog_id": 1,  # Include the blog_id field
                    "_id": 0       # Exclude the _id field
                }
            }
        ])
        
        similar_blogs = []
        for blog in similar_blogs_id:
            #skip if the blog_id is same as the sample blog
            if blog["blog_id"] == sample_blog["blog_id"]:
                continue
            t_blog = self.blogs.find_one({"blog_id": blog["blog_id"]})
            similar_blogs.append(Blog.from_dict(t_blog))
        
        return similar_blogs
    
    def get_recent_blogs(self, n=5):
        blogs = self.blogs.find().sort("date", -1).limit(n)
        return [Blog.from_dict(blog) for blog in blogs]
    
    def get_blog(self, blog_id):
        blog = self.blogs.find_one({"blog_id": blog_id})
        return Blog.from_dict(blog)
    
    def create_blog(self, content , title, author, categories, author_id):
        blog_id = self.blogs.count_documents({}) + 1
        blog = {
            "blog_id": blog_id,
            "title": title,
            "author": author,
            "content": content,
            "categories": categories,
            "date": datetime.datetime.now(),
            "author_id": author_id
        }
        self.blogs.insert_one(blog)
        self.generate_embeddings(blog["blog_id"])

    def update_blog(self, blog_id , content , title , categories):
        old_blog = self.blogs.find_one({"blog_id": blog_id})
        blog = {
            "blog_id": blog_id,
            "title": title,
            "author": old_blog["author"],
            "content": content,
            "categories": categories,
            "date": old_blog["date"],
            "author_id": old_blog["author_id"]
        }
        self.blogs.update_one({"blog_id": blog_id}, {"$set": blog})
        self.generate_embeddings(blog_id)

    def delete_blog(self, blog_id):
        self.blogs.delete_one({"blog_id": blog_id})
        self.blogs_embeddings.delete_one({"blog_id": blog_id})

    def generate_embeddings(self, blog_id):
        blog = self.blogs.find_one({"blog_id": blog_id})
        embeddings = OllamaEmbeddings(model="nomic-embed-text")
        blog_text = " "

        for key in ["content", "title", "author", "categories"]:
            if key in blog and blog[key]:
                blog_text += blog[key]

        embedding = embeddings.embed_query(blog_text)
        if self.blogs_embeddings.find_one({"blog_id": blog["blog_id"]}):
            self.blogs_embeddings.update_one({"blog_id": blog["blog_id"]}, {"$set": {"embedding": embedding}})
        else:
            self.blogs_embeddings.insert_one({"blog_id": blog["blog_id"], "embedding": embedding})
