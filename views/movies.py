from flask import request
from flask_restx import Resource, Namespace
from models import Movie, MovieSchema
from setup_db import db

movie_ns = Namespace('movies')

movies_schema = MovieSchema(many=True)


@movie_ns.route("/")
class MoviesView(Resource):
    def get(self):
        all_movies_query = db.session.query(Movie)

        director_id = request.args.get("director_id")
        if director_id:
            all_movies_query = all_movies_query.filter(Movie.director_id == director_id)

        genre_id = request.args.get("genre_id")
        if genre_id:
            all_movies_query = all_movies_query.filter(Movie.genre_id == genre_id)

        year_selected = request.args.get("year")
        if year_selected:
            all_movies_query = all_movies_query.filter(Movie.year == year_selected)

        final_query = all_movies_query.all()

        return movies_schema.dump(final_query), 200

    def post(self):
        new_data = request.json

        movie_ = movies_schema.load(new_data)
        new_movie = Movie(**movie_)
        with db.session.begin():
            db.session.add(new_movie)

        return "", 201

@movie_ns.route("/<mid>")
class MovieView(Resource):
    def get(self, mid):
        movie = Movie.query.get(mid)

        if not movie:
            return "", 404

        return movies_schema.dump(movie), 200

    def put(self, mid):
        movie_selected = db.session.query(Movie).filter(Movie.id == mid)
        movie_first = movie_selected.first()

        if movie_first is None:
            return "", 404

        new_data = request.json
        movie_selected.update(new_data)
        db.session.commit()

        return "", 204

    def delete(self, mid):
        movie_selected = db.session.query(Movie).filter(Movie.id == mid)
        movie_first = movie_selected.first()

        if movie_first is None:
            return "", 404

        rows_deleted = movie_selected.delete()
        if rows_deleted != 1:
            return "", 400

        db.session.commit()
        return "", 204
