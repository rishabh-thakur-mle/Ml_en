#main.py
from flask import Flask, request
from flask import jsonify
from contagion_calculator import ContagionCalculator
import os
app = Flask(__name__)


@app.route('/healthCheck/', methods=["GET"])
def health_check():
	response = {
	"healthcheck" : True
	}
	return jsonify(response)

@app.route('/', methods=["GET"])
def home():
	response = {
	"container" : "contagion_risk_calculator"
	}
	return jsonify(response)
                                                                                                                
@app.route('/contagion_risk/', methods=["POST"])
def event_trip_scoring():
	json_req = request.get_json()
	modeOfTransport = json_req["transitMode"]
	latlong_list = json_req["list"]
	contagion_object = ContagionCalculator(modeOfTransport,latlong_list)
	final_output = contagion_object.make_final_score()
	
	return jsonify(final_output)

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0',port = os.environ["PORT"])


##TO DO 
# 1. change import structure


