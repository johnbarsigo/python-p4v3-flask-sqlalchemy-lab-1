# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here

@app.route('/earthquakes/<int:id>', methods=['GET'])
def get_earthquake_by_id( id ):
    # response_body = f'{Earthquake.query.filter(Earthquake.id==id).first()}'
    # status_code = 200
    # headers={}

    # return make_response( response_body, status_code, headers)
    earthquake = Earthquake.query.get(id)
    
    if earthquake :
        returned = earthquake.to_dict()
        # return jsonify ({
        #     "id": earthquake.id,
        #     "location": earthquake.location,
        #     "magnitude": earthquake.magnitude,
        #     "year": earthquake.year
        # }), 200
        return returned, 200
    else :
        return jsonify({
            "message": f"Earthquake {id} not found."
        }), 404


@app.route('/earthquakes/magnitude/<float:magnitude>')
def earthquake_greater_magnitude ( magnitude ):
    earthquake = Earthquake.query.filter( Earthquake.magnitude >= magnitude ).all()
    count = len(earthquake)

    body = {
            "count" : count,
            "quakes" : [
                quake.to_dict() for quake in earthquake
                ]
            }
    # if earthquake :
    #     body = {
    #         "count" : count,
    #         "quakes" : [
    #             # {
    #             #     "id" : quake.id,
    #             #     "location" : quake.location,
    #             #     "magnitude" : quake.magnitude,
    #             #     "year" : quake.year
    #             # }
    #             quake.to_dict() for quake in earthquake
    #             ]
    #     }
    #     status = 200
    # else :
    #     body = {
    #         "count" : count,
    #         "quakes" : [ quake.to_dict() for quake in earthquake ]
    #     },
    #     status = 404

        # return jsonify ({
        #     "id" : earthquake.id,
        #     "location" : earthquake.location,
        #     "magnitude" : earthquake.magnitude,
        #     "year" : earthquake.year
        # }), 200
    # return (make_response( body, status ))
    return jsonify( body ), 200


if __name__ == '__main__':
    app.run(port=5555, debug=True)
