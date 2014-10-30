from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import backref, relationship
from sqlalchemy import ForeignKey
import correlation


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

    def similarity(self, other_user):

        # returns a correlation based on a list of paired ratings 
        # for each movie that 2 users have rated
        u_ratings = db_session.query(Rating).filter_by(user_id=self.id)
        
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
        
        return correlation.pearson(paired_ratings)

    def predict_rating(self, movie_id):
        m = db_session.query(Movie).get(movie_id)

        # if not u.ratings.movie_id:
        other_ratings = db_session.query(Rating).filter_by(movie_id = m.id).all()
        other_users = []

        for rating in other_ratings:
            other_users.append(rating.user)

        similarity_list = []

        for other_user in other_users:
            correlation = self.similarity(other_user)
            similarity_list.append((other_user.id, correlation))

        sorted_sim_list = sorted(similarity_list, key=lambda x: x[1])

        best_match_id, best_match_correlation = sorted_sim_list[-1]

        best_match_rating = db_session.query(Rating).filter_by(movie_id=movie_id).filter_by(user_id=best_match_id).one()

        predicted_rating = best_match_rating.rating * best_match_correlation
        return predicted_rating

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
    db_session = connect()
    main()
