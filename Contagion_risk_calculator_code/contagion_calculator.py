from data import quar_count_by_pins,master_latitude,master_longitude,master_pincode
import geopy.distance
import numpy as np


class ContagionCalculator:

	def __init__(self,mode_of_transport,latlong_list):
		self.mode_of_transport = mode_of_transport
		self.latlong_list =latlong_list
		self.transit_weight = .9
		if(self.mode_of_transport not in ("NOT_SPECIFIED")):
			if(self.mode_of_transport=="BUS"):
				self.transit_weight = .5
			elif(self.mode_of_transport in ["SUBWAY","TRAM"]):
				self.transit_weight = .4
			elif(self.mode_of_transport in ["TRAIN","RAIL"]):
				self.transit_weight =.3
			
	def return_score_latlong(self,latitude,longitude):
	    dictionary_latlong = {}
	    for i in range(len(master_latitude)):
	        coord_1 = (latitude,longitude)
	        coord_2 = (master_latitude[i],master_longitude[i])
	        dist = geopy.distance.distance(coord_1,coord_2).meters
	        if(dist<3000):
	            if(master_pincode[i] in dictionary_latlong.keys()):
	                if(dist<dictionary_latlong[master_pincode[i]]):
	                    dictionary_latlong[master_pincode[i]]=dist
	            else:
	            	dictionary_latlong[master_pincode[i]]=dist
	    return dictionary_latlong

	def calculate_score_and_radius(self,dictionary_latlong):
	    sum_scores =0
	    for pin in dictionary_latlong.keys():
	        sum_scores += quar_count_by_pins[pin]/dictionary_latlong[pin]
	        #print(sum_scores)
	    score  = 10*(1/(1+np.exp(-1*(1-self.transit_weight)*sum_scores)))
	    radius = ((score+1)/100) 
	    return score,radius

	def score_for_each_latlong(self):
		list_score  = []
		list_radius = []
		for latlong in self.latlong_list:
			latitude,longitude = float(latlong.split(",")[0]),float(latlong.split(",")[1])
			dictionary_latlong = self.return_score_latlong(latitude,longitude)
			score,radius 	   = self.calculate_score_and_radius(dictionary_latlong)
			list_score.append(score)
			list_radius.append(radius)
		return list_score,list_radius

	def make_final_score(self):
		list_score,list_radius = self.score_for_each_latlong()
		response_dictionary  = {}
		response_dictionary["overallScore"] = np.mean(list_score)
		locationlist = []
		for i in range(len(list_score)):
			dict_res = {}
			dict_res["locationScore"] = float(list_score[i])
			dict_res["radius"]		  = float(list_radius[i])
			dict_res["latitude"]      = float(self.latlong_list[i].split(",")[0])
			dict_res["longitude"]     = float(self.latlong_list[i].split(",")[1])
			locationlist.append(dict_res)
		response_dictionary["locationList"] = locationlist	
		return response_dictionary

if __name__ =="__main__":
	mode_of_transport ="BUS"
	latlong_list =["12.910434,77.607103","12.9121,77.6446","12.9352,77.6245"]
	contagion_object = ContagionCalculator(mode_of_transport,latlong_list)
	print(contagion_object.make_final_score())