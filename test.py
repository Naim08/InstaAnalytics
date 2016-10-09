import pickle

var = []
with open('savedDataSet','rb') as f:
	var = pickle.load(f)

print var[0]