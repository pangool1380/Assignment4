from flask import Flask
from flask import request
from flask import Response

from car_manager import CarManager

import json

app = Flask(__name__)

DB_NAME = "sqlite:///carlot.sqlite"


@app.route('/cars/all', methods=['GET'])
def get_all_cars():
    """ Gets all car records """

    car_mgr = CarManager(DB_NAME)
    cars = car_mgr.get_all_cars()
    car_list = []
    for car in cars:
        car_list.append(car.to_dict())
    return Response(json.dumps(car_list), mimetype='application/json')



    

@app.route('/cars', methods=['POST'])
def add_car():
    """ Adds a new car record """
    
    car_mgr = CarManager(DB_NAME)
    make = request.form['make']
    model = request.form['model']
    year = request.form['year']
    price = request.form['price']
    car_mgr.add_car(make, model, year, price)
    #if status is 200 then the car was added successfully or 400 if it was not
    return Response(status=200)
        
    
  
    
    


@app.route('/cars/<int:id>', methods=['DELETE'])
def delete_car(id):
    """ Deletes a car record """

    car_mgr = CarManager(DB_NAME)

    try:
        car_mgr.delete_car(id)

        response = app.response_class(status=200)

    
    except ValueError as e:
        response = app.response_class(response=str(e), status=404)

    return response


if __name__ == "__main__":
    app.run(debug=True)
