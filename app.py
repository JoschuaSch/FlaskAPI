from flask import Flask, jsonify, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
limiter = Limiter(app, key_func=get_remote_address)

books = [
    {"id": 1, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald"},
    {"id": 2, "title": "1984", "author": "George Orwell"},
    {"id": 3, "title": "To Kill a Mockingbird", "author": "Harper Lee"},
    {"id": 4, "title": "The Catcher in the Rye", "author": "J.D. Salinger"},
    {"id": 5, "title": "The Lord of the Rings", "author": "J.R.R. Tolkien"},
    {"id": 6, "title": "Pride and Prejudice", "author": "Jane Austen"},
    {"id": 7, "title": "The Hobbit", "author": "J.R.R. Tolkien"},
    {"id": 8, "title": "Animal Farm", "author": "George Orwell"},
    {"id": 9, "title": "The Kite Runner", "author": "Khaled Hosseini"},
    {"id": 10, "title": "Moby-Dick", "author": "Herman Melville"},
    {"id": 11, "title": "The Odyssey", "author": "Homer"},
    {"id": 12, "title": "Crime and Punishment", "author": "Fyodor Dostoevsky"},
    {"id": 13, "title": "The Iliad", "author": "Homer"},
    {"id": 14, "title": "War and Peace", "author": "Leo Tolstoy"},
    {"id": 15, "title": "Ulysses", "author": "James Joyce"},
    {"id": 16, "title": "The Inferno", "author": "Dante Alighieri"},
    {"id": 17, "title": "Les Misérables", "author": "Victor Hugo"},
    {"id": 18, "title": "The Count of Monte Cristo", "author": "Alexandre Dumas"},
    {"id": 19, "title": "Don Quixote", "author": "Miguel de Cervantes"},
    {"id": 20, "title": "Anna Karenina", "author": "Leo Tolstoy"}
]


def find_book_by_id(book_id):
    for book in books:
        if book["id"] == book_id:
            return book
    return None


def validate_book_data(data):
    if "title" not in data or "author" not in data:
        return False
    return True


@app.route('/api/books', methods=['GET', 'POST'])
@limiter.limit("2/minute")
def handle_books():
    if request.method == 'GET':
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        author = request.args.get('author')
        if author:
            filtered_books = [book for book in books if book.get('author') == author]
            paginated_books = filtered_books[(page - 1) * limit: page * limit]
        else:
            paginated_books = books[(page - 1) * limit: page * limit]
        return jsonify(paginated_books)
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
    book = find_book_by_id(book_id)
    if book is None:
        return '', 404
    books.remove(book)
    return jsonify(book)


@app.errorhandler(404)
def not_found_error(_):
    return jsonify({"error": "Not Found"}), 404


@app.errorhandler(405)
def method_not_allowed_error(_):
    return jsonify({"error": "Method Not Allowed"}), 405


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
