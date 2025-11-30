#!/usr/bin/env python3

from flask import request
from flask_restful import Resource
import os

from config import create_app, db, api
from models import Book, BookSchema

env = os.getenv("FLASK_ENV", "dev")
app = create_app(env)

class Books(Resource):
    def get(self):
        # simple pagination
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 5))
        query = Book.query.paginate(page=page, per_page=per_page, error_out=False)

        data = {
            "page": query.page,
            "per_page": query.per_page,
            "items": [BookSchema().dump(b) for b in query.items],
            "total": query.total,
            "total_pages": query.pages
        }
        return data, 200

api.add_resource(Books, '/books', endpoint='books')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
