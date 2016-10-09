import api

users = ["childofdhaka"]

for user in users:
	data = api.getPictures(user)
	#data1 = api.getPictures(user)
	# picture = api.getFirst10(user)
	print(len(data))