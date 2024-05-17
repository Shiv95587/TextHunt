import os
import shutil
from flask import jsonify, request, send_file
from utils import get_results, convert_to_json_output

def create_routes(app):
    
    @app.route('/file/<path:filename>')
    def serve_pdf(filename):
        return send_file(filename)
    
    @app.route('/members', methods=['POST'])
    def upload_files():
        if 'file' not in request.files:
            return 'No file part', 400

        files = request.files.getlist('file')

        for file in files:
            if file.filename == '':
                return 'No selected file', 400

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

        return jsonify({'message': 'Files uploaded successfully'}), 200

    @app.route('/process', methods=['GET'])
    def process_query():
        current_directory = os.getcwd()
        files = os.listdir(current_directory)
        for file in files:
            if file.startswith("highlighted_"):
                os.remove(os.path.join(current_directory, file))

        query = request.args.get('query')
        isWordSearch = request.args.get('isWordSearch')
        directory = 'uploads/'
        file_paths = [os.path.join(directory, file) for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file))]

        results = get_results(query, file_paths, isWordSearch)
        results = convert_to_json_output(results)

        return jsonify({'results': results})
