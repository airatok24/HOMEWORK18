from flask import request
from flask_restx import Resource, Namespace
from models import Genre, GenreSchema
from setup_db import db

genre_ns = Namespace('genres')

genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)


@genre_ns.route("/")
class GenresView(Resource):
    def get(self):
        query_all = db.session.query(Genre)
        final_query = query_all.all()

        return genres_schema.dump(final_query), 200

    def post(self):
        new_data = request.json
        new_genre = Genre(new_data)
        with db.session.begin():
            db.session.add(new_genre)

        return "", 201


@genre_ns.route("/<int:gid>")
class GenreView(Resource):
    def get(self, gid):
        query_one = Genre.query.get(gid)

        if not query_one:
            return "", 404

        return genre_schema.dump(query_one), 200

    def put(self, gid):
        genre_selected = db.session.query(Genre).filter(Genre.id == gid)
        genre_first = genre_selected.first()

        if genre_first is None:
            return "", 404

        new_data = request.json
        genre_selected.update(new_data)
        db.session.commit()

        return "", 204

    def delete(self, gid):
        genre_selected = db.session.query(Genre).filter(Genre.id == gid)
        genre_first = genre_selected.first()

        if genre_first is None:
            return "", 404

        rows_deleted = genre_selected.delete()
        # если произошло удаление более 1 строки, то указываем на наличие проблемы.
        if rows_deleted != 1:
            return "", 400

        db.session.commit()
        return "", 204
