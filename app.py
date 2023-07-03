from flask import Flask, jsonify, request

app = Flask(__name__)

books = [
    {"id": 1, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald"},
    {"id": 2, "title": "1984", "author": "George Orwell"}
]


def find_book_by_id(book_id):
    """Find a book by its ID in the `books` list."""
    for book in books:
        if book["id"] == book_id:
            return book
    return None


def validate_book_data(data):
    """Check that the required book fields (title and author) are in the data."""
    if "title" not in data or "author" not in data:
        return False
    return True


@app.route('/api/books', methods=['GET', 'POST'])
def handle_books():
    """
    Handle GET and POST requests to '/api/books'.

    GET: Return a list of all books.
    POST: Add a new book to the list and return the added book, if the book data is valid.
    """
    if request.method == 'GET':
        return jsonify(books)
    elif request.method == 'POST':
        new_book = request.get_json()
        if not validate_book_data(new_book):
            return jsonify({"error": "Invalid book data"}), 400
        new_id = max(book['id'] for book in books) + 1
        new_book['id'] = new_id
        books.append(new_book)
        return jsonify(new_book), 201


@app.route('/api/books/<int:book_id>', methods=['PUT'])
def handle_book(book_id):
    """
    Handle PUT request to '/api/books/<book_id>'.

    Update the book with the given ID using data from the request.
    If the book isn't found, return a 404 error.
    """
    book = find_book_by_id(book_id)
    if book is None:
        return '', 404
    new_data = request.get_json()
    for key in new_data:
        if key in book:
            book[key] = new_data[key]
    return jsonify(book)


@app.route('/api/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    """
    Handle DELETE request to '/api/books/<book_id>'.

    Remove the book with the given ID from the list.
    If the book isn't found, return a 404 error.
    """
    book = find_book_by_id(book_id)
    if book is None:
        return '', 404
    books.remove(book)
    return jsonify(book)


@app.errorhandler(404)
def not_found_error(_):
    """
    Handle 404 errors.

    Return a JSON response with an error message.
    """
    return jsonify({"error": "Not Found"}), 404


@app.errorhandler(405)
def method_not_allowed_error(_):
    """
    Handle 405 errors.

    Return a JSON response with an error message.
    """
    return jsonify({"error": "Method Not Allowed"}), 405


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
