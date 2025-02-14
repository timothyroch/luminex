from flask import Flask, jsonify # type: ignore

app = Flask(__name__)

# Define custom error classes
class APIError(Exception):
    """Base class for API-specific errors."""
    def __init__(self, message, status_code):
        super().__init__(message)
        self.message = message
        self.status_code = status_code

class BadRequestError(APIError):
    """Error for bad requests (400)."""
    def __init__(self, message="Bad Request"):
        super().__init__(message, 400)

class UnauthorizedError(APIError):
    """Error for unauthorized access (401)."""
    def __init__(self, message="Unauthorized"):
        super().__init__(message, 401)

class ForbiddenError(APIError):
    """Error for forbidden actions (403)."""
    def __init__(self, message="Forbidden"):
        super().__init__(message, 403)

class NotFoundError(APIError):
    """Error for resources not found (404)."""
    def __init__(self, message="Not Found"):
        super().__init__(message, 404)

class InternalServerError(APIError):
    """Error for server-side issues (500)."""
    def __init__(self, message="Internal Server Error"):
        super().__init__(message, 500)

# Register error handlers
@app.errorhandler(APIError)
def handle_api_error(error):
    """
    Handles API-specific errors and returns a JSON response.
    """
    response = jsonify({
        "error": {
            "message": error.message,
            "status_code": error.status_code
        }
    })
    response.status_code = error.status_code
    return response

@app.errorhandler(400)
def handle_bad_request(error):
    """
    Handles generic bad requests and returns a JSON response.
    """
    return jsonify({"error": {"message": "Bad Request", "status_code": 400}}), 400

@app.errorhandler(404)
def handle_not_found(error):
    """
    Handles resource not found errors and returns a JSON response.
    """
    return jsonify({"error": {"message": "Not Found", "status_code": 404}}), 404

@app.errorhandler(500)
def handle_internal_server_error(error):
    """
    Handles internal server errors and returns a JSON response.
    """
    return jsonify({"error": {"message": "Internal Server Error", "status_code": 500}}), 500

# Example usage with routes
@app.route("/example", methods=["GET"])
def example_endpoint():
    """
    An example endpoint to demonstrate error handling.
    """
    raise BadRequestError("This is an example of a bad request.")

@app.route("/protected", methods=["GET"])
def protected_endpoint():
    """
    An example endpoint to demonstrate unauthorized error handling.
    """
    raise UnauthorizedError("You are not authorized to access this resource.")

if __name__ == "__main__":
    app.run(debug=True, port=5007)
