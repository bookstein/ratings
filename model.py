from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import backref, relationship
from sqlalchemy import ForeignKey


ENGINE = None
Session = None

Base = declarative_base()


### Class declarations go here

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True)
    email = Column(String(120), nullable=True)
    password = Column(String(60), nullable=True)
    age = Column(Integer, nullable=True)
    zipcode = Column(String(15), nullable=True)
    occupation = Column(String(60), nullable=True)

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key = True)
    title = Column(String(120))
    release_date = Column(Date)
    url = Column(String(120))

class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key = True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable = False)
    movie_id = Column(Integer, ForeignKey('movies.id'), nullable = False)
    rating = Column(Integer, nullable = False)

    user = relationship("User", backref=backref("ratings", order_by=id))
    movie = relationship("Movie", backref=backref("ratings", order_by=rating))
    
    # ratings is a backref from the Rating class


def get_paired_ratings(user, other_user):
    # returns a list of paired ratings for each movie that 2 users have rated
    u_ratings = db_session.query(Rating).filter_by(user_id=user.id)
    
    u_rating_dict = {}
    for rating in u_ratings:
        u_rating_dict[rating.movie_id] = rating.rating
    
    o_ratings = db_session.query(Rating).filter_by(user_id=other_user.id)

    paired_ratings = []
    for o_rating in o_ratings:
        match = u_rating_dict.get(o_rating.movie_id)
        if match:
            pair = (match, o_rating.rating)
            paired_ratings.append(pair)
    return paired_ratings

### End class declarations

def connect():
    global ENGINE
    global Session 

    ENGINE = create_engine("sqlite:///ratings.db", echo=True)
    Session = sessionmaker(bind=ENGINE)

    return Session()

def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__":
    main()
