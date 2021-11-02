from flask import Blueprint, jsonify, make_response, request
from app import db
from app.models.book import Book

# Creating book blueprint
books_bp = Blueprint("books_bp", __name__, url_prefix="/books")

@books_bp.route("", methods=["POST", "GET"])
def handle_books():
    if request.method == "POST": 
        request_body = request.get_json()
        if "title" not in request_body or "description" not in request_body:
            return make_response("Invalid Request", 400)

        new_book = Book(
            title=request_body["title"],
            description=request_body["description"]
        )
        db.session.add(new_book)
        db.session.commit()

        return f"Book {new_book.title} created", 201

    elif request.method == "GET":
        title_from_url = request.args.get("title")
        # if request.args.get("title"):
        if title_from_url:
            books = Book.query.filter_by(title=title_from_url)
        # elif request.args.get("description"):
        else:
            books = Book.query.all()

        books_response = []
        for book in books:
            books_response.append(
                {
                    "id": book.id,
                    "title": book.title,
                    "description": book.description
                }
            )
        return jsonify(books_response)

@books_bp.route("/<book_id>", methods=["GET", "PUT", "DELETE"])
def handle_book(book_id):
    book = Book.query.get(book_id) # Used db to get book by ID

    # Either I get a book back or None
    if book is None:
        return make_response(f"Book {book_id} not found", 404)
    
    if request.method == "GET":
        return {
            "id": book.id,
            "title": book.title,
            "description": book.description
            }

    elif request.method == "PUT":
        request_body = request.get_json() # just return request body (strip headers)

        try:
            book.title = request_body["title"]
            book.description = request_body["description"]

            db.session.commit() # save into database
            return {
                "message": "Book with {book.title} has been successfully updated"
                }, 200
        except KeyError:
            return {
                "message": "Request requires both 'title' and 'description'"
            }, 400

    elif request.method == "DELETE":
        db.session.delete(book)
        db.session.commit()
        return {
            "message": "Book with {book.title} has been deleted"
        }, 200