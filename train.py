import api
# import pandas as pd
import json
from clarifai.client import ClarifaiApi
clarifai_api = ClarifaiApi()
from sklearn.linear_model import LinearRegression

users = ["naimmiah08"]

tag_pool = []

users_omega = {}

images = []
likes = []

for user in users:
	data = api.getData(user)
	# media = api.getPictures(user)
	media = data["media"]["nodes"]
	image_links = []
	for mediaItem in media:
		image_links.append(mediaItem["display_src"])
	results = clarifai_api.tag_image_urls(image_links)["results"]
	for result in results:
		result = result["result"]["tag"]
		tag_pool.extend(result["classes"])
	users_omega[user] = results
list(set(tag_pool))

for user in users_omega:
	data = api.getData(user)
	follows = data["follows"]["count"]
	followed_by = data["followed_by"]["count"]
	bio = data["biography"]
	media = data["media"]["nodes"]
	results = users_omega[user]
	i = 0
	features = []
	for result in results:
		result = result["result"]["tag"]
		item = media[i]
		likes.append(item["likes"]["count"])
		caption = item["caption"]
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
		i = i + 1
	images.append(features)

linearClassifier = LinearRegression()
linearClassifier.fit(images, likes)