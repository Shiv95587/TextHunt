# from flask import Flask,jsonify,request,  send_from_directory, send_file
# from flask_cors import CORS
# import os
# import fitz
# import re
# import nltk
# from PIL import Image
# from PIL import Image, ImageDraw
# from reportlab.lib.pagesizes import letter
# from reportlab.pdfgen import canvas
# from nltk.stem import PorterStemmer
# from nltk.corpus import stopwords
# from nltk.tokenize import word_tokenize
# from nltk.stem import WordNetLemmatizer
# from collections import Counter
# from paddleocr import PaddleOCR
# from collections import defaultdict
# import numpy as np
# import base64
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
# import shutil


# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')
# ocr = PaddleOCR(use_angle_cls=True, lang='en')
# app =Flask(__name__)
# CORS(app)


# @app.route('/file/<path:filename>')
# def serve_pdf(filename):
#     return send_file(filename)


# UPLOAD_FOLDER = 'uploads'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# @app.route('/members', methods=['POST'])
# def upload_files():
#     # Ensure that files were sent in the request
#     if 'file' not in request.files:
#         return 'No file part', 400

#     # Retrieve the list of files from the request
#     files = request.files.getlist('file')

#     # Iterate over the list of files
#     for file in files:
#         # Check if the file name is not empty
#         if file.filename == '':
#             return 'No selected file', 400

#         # Save each file to the upload folder
#         file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

#     # Return a success message
#     return jsonify({'message': 'Files uploaded successfully'}), 200


# @app.route('/process', methods=['GET'])
# def process_query():
    

#     # Get the current directory
#     current_directory = os.getcwd()

#     # List all files in the directory
#     files = os.listdir(current_directory)
#     print(files)

#     for file in files:
#         # Check if the file starts with "highlighted_"
#         if file.startswith("highlighted_"):
#             os.remove(os.path.join(current_directory, file))

#     query = request.args.get('query')
#     isWordSearch = request.args.get('isWordSearch')
#     print('word search', isWordSearch)
#     print("Hello I am ", query)
#     directory = 'uploads/'
#     file_paths = [os.path.join(directory, file) for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file))]

#     print(file_paths)
#     input_documents = file_paths
#     print(isWordSearch)
#     results = get_results(query, input_documents, isWordSearch)    
#     print(results)

#     results = convert_to_json_output(results)
#     # return jsonify({'query': query})
#     return jsonify({'results': results})

# def convert_to_json_output(results):
#     result = []

#     for file_paths, numbers in results.items():
#         result.append([file_paths,list(numbers)])
#     return result

# def save_pdf_to_directory(source_pdf, destination_directory):
#     try:
#         shutil.copy(source_pdf, destination_directory)
#         print("PDF saved successfully.")
#     except Exception as e:
#         print("Error:", e)

# def get_results(query, input_documents, isWordSearch):
#     print(query)
#     print("isWordSearch:", isWordSearch)
    
#     if isWordSearch.lower() == 'true':
#         print("Performing word search")
#         tokens = query.split()
#         query = preprocess_query(query)
#         query = preprocess_text(query, PorterStemmer())
#         tokens = set(tokens)
#         print("Tokens are:", tokens)
#         ranked_documents = get_relevant_results(query, input_documents)
#         results = get_relevant_docs_with_pageno(ranked_documents, tokens)
#         return results
#     else:
#         print("Performing phrase search")
#         results = get_phrase_match(query, input_documents)
#         print(results)
#         return results


# def get_filename(doc_path):
#     return doc_path.split("/")[-1]

# def get_relevant_docs_with_pageno(ranked_documents,tokens):
#     results = defaultdict(set)
#     for similarity, doc_path in ranked_documents:
#         if similarity > 0:
#             if isPdf(doc_path):
#                 pdf_document = fitz.open(doc_path)
#                 for page_num in range(len(pdf_document)):
#                     page = pdf_document[page_num]
#                     words = page.get_text("words")
#                     for word in words:
#                         word_text = word[4] # word text
#                         # highlight complete word on pdf
#                         for token in tokens:
#                             if token.lower() in word_text.lower():
#                                 results[get_highlighted_file_output_path(doc_path)].add(page_num + 1)
#                                 text_instances = page.search_for(word_text)
#                                 for instance in text_instances:
#                                     page.add_highlight_annot(instance)
#                                 break
#                 # Save the modified PDF
#                 pdf_document.save(get_highlighted_file_output_path(doc_path))
#                 pdf_document.close()
#             elif isImage(doc_path):
#                 highlight_text_in_image(tokens, doc_path, results)
#                 print("Image ocred")

#     return results


# def get_highlighted_file_output_path(doc_path):
#     return "highlighted_" + doc_path.split("/")[-1]

# def preprocess_query(query):
#     query = query.lower()
#     query = re.sub(r'[^a-zA-Z\s]', '', query)
#     return query

# def preprocess_text(text, porter_stemmer):
#     text = text.lower()
#     # Tokenize text
#     text = re.sub(r'[^a-zA-Z\s]', '', text)
#     tokens = word_tokenize(text.lower())
#     # Apply stemming using Porter Stemmer
#     stemmed_tokens = [porter_stemmer.stem(token) for token in tokens if token.isalnum()]
#     # Join stemmed tokens back into text
#     stemmed_text = ' '.join(stemmed_tokens)
#     return stemmed_text

# def ocr_image(img_path):
#     result = ocr.ocr(img_path, cls=True)
#     # Print the OCR result
#     recognized_text = ""
#     prev = []
#     for line in result:
#         for word in line:
#             text = word[1][0]
#             recognized_text += text + " "
#     return recognized_text

# def isPdf(document):
#     return document.split(".")[-1] == "pdf"

# def isImage(document):
#     return document.split(".")[-1] in ('jpg', 'png', 'jpeg')

# def get_text_from_pdf(pdf_path):
#     pdf_document = fitz.open(pdf_path)
#     text = ""
#     for page_num in range(len(pdf_document)):
#         page = pdf_document[page_num]
#         text += page.get_text()
#     return text   

# # This searches the phrase in the documents
# def get_phrase_match(query, input_documents):
#     relevant_docs = defaultdict(set)
#     print(input_documents)
#     print("Hi")
#     for i in range(len(input_documents)):
#         is_matched = False
#         if isPdf(input_documents[i]):
#             pdf_document = fitz.open(input_documents[i])
#             for page_num in range(len(pdf_document)):
#                 page = pdf_document[page_num]    
#                 # Search for the word on the page
#                 text_instances = page.search_for(query)
#                 if len(text_instances) > 0:
#                     is_matched = True
#                     relevant_docs[get_highlighted_file_output_path(input_documents[i])].add(page_num + 1)
#                 # Highlight each instance of the word
#                 for instance in text_instances:
#                     page.add_highlight_annot(instance)
#             # Save the modified PDF
#             if is_matched:
#                 output_path = get_highlighted_file_output_path(input_documents[i])
#                 pdf_document.save(output_path)
#             pdf_document.close()
#         elif isImage(input_documents[i]):
#             text = ocr_image(input_documents[i])
#             if query.lower() in text.lower():
#                 relevant_docs[get_highlighted_file_output_path(input_documents[i])].add(1)
#                 image = Image.open(input_documents[i])
#                 draw = ImageDraw.Draw(image)
#                 output_path = get_highlighted_file_output_path(input_documents[i])
#                 image.save(output_path)
#     return relevant_docs

# def get_relevant_results(query, input_documents):
#     docs = []
#     porter_stemmer = PorterStemmer()
    
#     for i in range(len(input_documents)):
#         if isPdf(input_documents[i]):
#             text = get_text_from_pdf(input_documents[i])
#             stemmed_text = preprocess_text(text, porter_stemmer)
#             docs.append(stemmed_text)
#         else:
#             text = ocr_image(input_documents[i])
#             stemmed_text = preprocess_text(text, porter_stemmer)
#             docs.append(stemmed_text)

#     results = proximity_search(query, docs, input_documents)
#     print("Documents relevant to the query:")
#     for similarity, doc in results:
#         print(f"Similarity: {similarity}, Document: {doc}")
#     return results

# def proximity_search(query, documents, doc_paths):
#     # Vectorize documents using TF-IDF
#     tfidf_vectorizer = TfidfVectorizer(stop_words='english')
#     tfidf_matrix = tfidf_vectorizer.fit_transform(documents)
#     # Vectorize query using the same vocabulary
#     query_vector = tfidf_vectorizer.transform([query])
#     # Calculate cosine similarity between query and documents
#     similarities = cosine_similarity(query_vector, tfidf_matrix)
#     # Sort documents by similarity scores
#     ranked_docs = sorted(zip(similarities[0], doc_paths), reverse=True)
#     return ranked_docs

# def highlight_text_in_image(tokens, doc_path,results):
#     # Open the image
#     image = Image.open(doc_path)
#     draw = ImageDraw.Draw(image)
#     result = ocr.ocr(doc_path, cls=True)
#     for line in result[0]:
#         detected_word = line[1][0]
#         for word in tokens:
#             if detected_word.lower().find(word.beckend/server.pylower()) != -1:
#                 results[get_highlighted_file_output_path(doc_path)].add(1)
#                 bbox = line[0]
#                 points = [int(coord) for xy_pair in bbox for coord in xy_pair]
#                 points = [(points[i], points[i + 1]) for i in range(0, len(points), 2)]
#                 draw.polygon(points, outline="red")
#     image.save(get_highlighted_file_output_path(doc_path))
# if __name__=="__main__":
#     app.run(debug=True)