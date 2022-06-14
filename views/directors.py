from flask import request
from flask_restx import Resource, Namespace
from models import Director, DirectorSchema
from setup_db import db

director_ns = Namespace('directors')

director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)


@director_ns.route("/")
class DirectorsView(Resource):
    def get(self):
        query_all = db.session.query(Director)
        final_query = query_all.all()

        return directors_schema.dump(final_query), 200

    def post(self):
        new_data = request.json

        director_ = director_schema.load(new_data)
        with db.session.begin():
            db.session.add(director_)

        return "", 201
    # ставим при проверке закрывающий слэш в Postman


new_director = {"name": "Шеридан Шеридан"}


@director_ns.route("/<int:did>")
class DirectorView(Resource):
    def get(self, did):
        query_one = Director.query.get(did)

        if not query_one:
            return "", 404

        return director_schema.dump(query_one), 200

    def put(self, did):
        director_selected = db.session.query(Director).filter(Director.id == did)
        director_first = director_selected.first()

        if director_first is None:
            return "", 404

        new_data = request.json
        director_selected.update(new_data)
        db.session.commit()

        return "", 204

    def delete(self, did):
        director_selected = db.session.query(Director).filter(Director.id == did)
        director_first = director_selected.first()

        if director_first is None:
            return "", 404

        rows_deleted = director_selected.delete()
        if rows_deleted != 1:
            return "", 400

        db.session.commit()
        return "", 204
