from car import Car

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class CarManager:
    """Manager of car records """

    def __init__(self, db_name):

        if db_name is None or db_name == "":
            raise ValueError("Invalid database name")

        engine = create_engine(db_name)
        self._db_session = sessionmaker(bind=engine)

    def add_car(self, make, model, year, price):
        """Adds a Single car """

        if make is None or make == "":
            raise ValueError("Make must be defined")

        if model is None or model == "":
            raise ValueError("Model must be defined")

        if year is None or year == "":
            raise ValueError("Year must be defined")

        if price is None or price == "":
            raise ValueError("Price must be defined")

        car = Car(make, model, year, price)
        session = self._db_session()
        session.add(car)
        session.commit()
        session.close()


    def delete_car(self, id): 
        """" Deletes a single car based on the id """

        if id is None or id == "":
            raise ValueError("Id must be defined")

        session = self._db_session()
        car = session.query(Car).filter_by(id=id).first()
        if car is None:
            raise ValueError("Id must be positive")
        session.delete(car)
        session.commit()
        session.close()



    def get_all_cars(self):
        """Returns a list of all cars """

        session = self._db_session()
        cars = session.query(Car).all()
        session.close()
        return cars