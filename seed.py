"""Utility file to seed ratings database from MovieLens data in seed_data/"""

from sqlalchemy import func
from model import User
from model import Rating
from model import Movie
from datetime import datetime

from model import connect_to_db, db
from server import app


def load_users():
    """Load users from u.user into database."""

    print "Users"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    User.query.delete()

    # Read u.user file and insert data
    for row in open("seed_data/u.user"):
        row = row.rstrip()
        user_id, age, gender, occupation, zipcode = row.split("|")

        user = User(user_id=user_id,
                    age=age,
                    zipcode=zipcode)

        # We need to add to the session or it won't ever be stored
        db.session.add(user)

    # Once we're done, we should commit our work
    db.session.commit()


def load_movies():
    """Load movies from u.item into database."""

    Movie.query.delete()

    # Read u.item file and insert data
    for row in open("seed_data/u.item"):
        row = row.rstrip()
        row = row.split("|")

        #unpack the string in to variables, deal with the title later
        movie_id, title, s, empty_string, imbd_url = row[:5]

        # date = title[-5:-1]
        title = title[:-7]

        #using string parse time to to turn a string in to a datetime object
        d = datetime.strptime(s, "%d-%b-%Y")

        #add a single row in the the movie table for each line in the u.item file.
        movie = Movie(movie_id=int(movie_id),
                      title=title,
                      released_at=d,
                      imbd_url=imbd_url)

        # Add to the session or it won't ever be stored
        db.session.add(movie)

    # Once we're done, we should commit our work
    db.session.commit()


def load_ratings():
    """Load ratings from u.data into database."""

    Rating.query.delete()

    # Read u.item file and insert data
    for row in open("seed_data/u.data"):
        row = row.rstrip()
        rating_id, movie_id, user_id, score = row.split()
        #this will return a list for each row, the list will include four strings each.
        #one string for each rating_id, movie_id, user_id and score

        #adding a single row in the rating table for each line in the u.data txt file.
        rating = Rating(rating_id=int(rating_id),
                        movie_id=int(movie_id),
                        user_id=int(user_id),
                        score=int(score))

        # Add to the session or it won't ever be stored
        db.session.add(rating)

    # Once we're done, we should commit our work
    db.session.commit()


def set_val_user_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_users()
    load_movies()
    load_ratings()
    set_val_user_id()
