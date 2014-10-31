from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm import backref, relationship
from sqlalchemy import ForeignKey
import correlation



ENGINE = create_engine("sqlite:///ratings.db", echo=True)
db_session = scoped_session(sessionmaker(bind=ENGINE, autocommit=False, autoflush = False))

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
        
        similarity_list = []
        for rating in m.ratings:
            correlation = self.similarity(rating.user)
            if correlation > 0:
                similarity_list.append((rating.rating, correlation))

        weighted_mean = sum(map(lambda x: x[0]*x[1], similarity_list)) / sum(map(lambda x: x[1], similarity_list))

        return weighted_mean

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
   

def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__":
    db_session = connect()
    main()
