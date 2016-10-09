import api
import pickle
from sklearn.linear_model import LinearRegression
from pymongo import MongoClient
users = ["childofdhaka"]
client = MongoClient()
db = client.instagram

#for user in users:
#    #data = api.getPictures(user)
#    data1 = api.getData(user)
#    #picture = api.getFirst10(user)
#    data2 = api.getFollowers(user, data1['followed_by']['count'])
#    print(data2)
var = []
with open('savedDataSet','rb') as f:
    var = pickle.load(f)

getTags = db.tags_pool.find()
for tags in getTags:
    print tags['tags']

linearClassifier = LinearRegression()
linearClassifier.fit(var[0], var[1])