from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Date

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
    user_id = Column(Integer, nullable = False)
    movie_id = Column(Integer, nullable = False)
    rating = Column(Integer, nullable = False)

### End class declarations

def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__":
    main()
