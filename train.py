import api
# import pandas as pd
import json
import numpy as np
#from clarifai.client import ClarifaiApi
#clarifai_api = ClarifaiApi()
from clarifai import rest
from clarifai.rest import ClarifaiApp
from pymongo import MongoClient
import pickle
app = ClarifaiApp("v8Czk2boQhiop51nZ0R4R4L4Wpohwb9ZyvUGKdvC", "Hh6kZKeYLdOwu0LsgT6eML_pzVxX_gasdvkT07cD")
model = app.models.get("general-v1.3")
client = MongoClient()
db = client.instagram

users = [
	"naimmiah08",
    "ohmytousif",
	"childofparis",
	"mushref_hussain",
	"childofdhaka",
	# "syedfordeys", 
	# "zabibee",  
	# "birdpanda",  
	# "clitoristal",  
	# "sub.a",  
	# "tif.lon",  
	# "bethybogart",  
	# "mfazalul",  
	# "syedmuhtasim",  
	# "micaluvv",  
	# "saxtothemax",  
	# "beenoohh",  
	# "sneaky_potato",  
	# "moesaucesome",  
	# "isha.mehra",  
	# "kris_mc_",  
	# "fatalraven", 
	# "themacintosh1", 
	# "mulla.man",  
	# "lilmissshine124",  
	# "the_manamina",  
	# "emptyconvos",  
	# "throwrw male",  
	"a.rah_man",  
	"hassaniboii",   
	# "ahad_sheriff",   
	# "ammaarica",   
	# "humii9",  
	# "childofdhaka" 
]

tag_pool = []

users_omega = {}

images = []
likes = []

following = []
followers = []

max_clarifai_limit = 128

# predict with the model
for user in users:
	print "Doing user " + user
	data = api.getData(user)
	media = api.getPictures(user)
	# media = data["media"]["nodes"]
	image_links = []
	results = []
	for mediaItem in media:
		image_links.append(mediaItem["display_src"])
		imageinfo = model.predict_by_url(mediaItem["display_src"])
		classes = []
		probs = []
		for i in imageinfo['outputs'][0]['data']['concepts']:
			classes.append(i['name'])
			probs.append(i['value'])
		results.append({'result': {'tag': {'classes': classes, 'probs': probs}}})
		classes = []
		probs = []
	#    print results
	#    if len(image_links) > max_clarifai_limit:
	#        times = image_links % max_clarifai_limit
	#    else:
	#        results = clarifai_api.tag_image_urls(image_links)["results"]
	#        print(results)
	for result in results:
		result = result["result"]["tag"]
		tag_pool.extend(result["classes"])
	users_omega[user] = results
tag_pool = set(tag_pool)

db.tags_pool.update({'id': 1}, { '$set' : {'tags': list(tag_pool)}})

for user in users_omega:
	data = api.getData(user)
	follows = data["follows"]["count"]
	followed_by = data["followed_by"]["count"]
	bio = data["biography"]
	media = api.getPictures(user)
	# media = data["media"]["nodes"]
	results = users_omega[user]
	i = 0
	for result in results:
		features = []
		result = result["result"]["tag"]
		item = media[i]
		likes.append(item["likes"]["count"])
		#caption = item["caption"]
		classes = result["classes"]
		probs = result["probs"]
		for tag in tag_pool:
			if tag in classes:
				features.append(1)
				idx = classes.index(tag)
				features.append(probs[idx])
			else:
				features.append(0)
				features.append(0)
		features.append(follows)
		features.append(followed_by)
		following.append(follows)
		followers.append(followed_by)
		i = i + 1
		images.append(features)

follows_median = np.median(follows)
followers_median = np.median(followers)

for image in images:
	follows_idx = len(image)-2
	followers_idx = len(image)-1
	image[follows_idx] = image[follows_idx] >= follows_idx
	image[followers_idx] = image[followers_idx] >= followers_median

print len(images[0])
with open('savedDataSet', 'wb') as f:
	dataset = [images, likes, follows_median, followers_median]
	pickle.dump(dataset, f)