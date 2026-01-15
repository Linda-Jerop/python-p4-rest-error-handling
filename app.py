from flask import Flask, make_response, jsonify
from werkzeug.exceptions import NotFound, BadRequest, InternalServerError

app = Flask(__name__)

# Simulating a database using a small dict
BOOKS = {
    1: {"id": 1, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald"},
    2: {"id": 2, "title": "To Kill a Mockingbird", "author": "Harper Lee"},
    3: {"id": 3, "title": "1984", "author": "George Orwell"},
}


@app.route("/books", methods=["GET"])
def get_books():
    return make_response(jsonify(list(BOOKS.values())), 200)



@app.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    if book_id not in BOOKS:
        raise NotFound(f"Book with ID {book_id} not found.")
    
    return make_response(jsonify(BOOKS[book_id]), 200)



@app.route("/books", methods=["POST"])
def create_book():
    new_id = 1
    
    if new_id in BOOKS:
        raise BadRequest(f"A book with ID {new_id} already exists.")
    
    return make_response(jsonify({"message": "Book created"}), 201)



# === ERROR HANDLERS ===

@app.errorhandler(NotFound)
def handle_not_found(e):
    """
    Handle 404 Not Found errors.
    Called when a client requests a resource that doesn't exist.
    """
    # Create a response with detailed error message
    response = make_response(
        jsonify({
            "error": "Not Found",
            "message": str(e.description),
            "status_code": 404
        }),
        404
    )
    return response


@app.errorhandler(BadRequest)
def handle_bad_request(e):
    """
    Handle 400 Bad Request errors.
    Called when the client sends invalid data or makes a bad request.
    """
    # Provide helpful feedback to the client about what went wrong
    response = make_response(
        jsonify({
            "error": "Bad Request",
            "message": str(e.description),
            "status_code": 400
        }),
        400
    )
    return response


@app.errorhandler(InternalServerError)
def handle_internal_server_error(e):
    """
    Handle 500 Internal Server Error.
    Called when something goes wrong on the server side.
    """
    # Alert the client that it's a server error, not their fault
    response = make_response(
        jsonify({
            "error": "Internal Server Error",
            "message": "Something went wrong on our end. Please try again later.",
            "status_code": 500
        }),
        500
    )
    return response


@app.errorhandler(Exception)
def handle_generic_error(e):
    """
    Catch-all error handler for any unhandled exceptions.
    This ensures that even unexpected errors return a proper response.
    """
    # Return a 500 error with a generic message for unexpected errors
    response = make_response(
        jsonify({
            "error": "Internal Server Error",
            "message": "An unexpected error occurred. Please contact support.",
            "status_code": 500
        }),
        500
    )
    return response


# Run the application if this file is executed directly
if __name__ == "__main__":
    app.run(debug=True)
