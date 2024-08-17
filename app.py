from flask import Flask
from flask_cors import CORS
from routes.blog_routes import blog_bp
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Register the blueprint with a URL prefix
app.register_blueprint(blog_bp, url_prefix='/api')

if __name__ == "__main__":
    app.run(debug=True)
