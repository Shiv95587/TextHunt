from flask import Flask
from flask_cors import CORS
from routes import create_routes

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create routes
create_routes(app)

if __name__ == "__main__":
    app.run(debug=True)
