import os 
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import api
from werkzeug import secure_filename
from clarifai import rest
from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage
import api
from pymongo import MongoClient
appApi = ClarifaiApp("v8Czk2boQhiop51nZ0R4R4L4Wpohwb9ZyvUGKdvC", "Hh6kZKeYLdOwu0LsgT6eML_pzVxX_gasdvkT07cD")
model = appApi.models.get("general-v1.3")
app = Flask(__name__)
client = MongoClient()
db = client.instagram


# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = 'uploads/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/test")
def rerouteTest():
	return redirect("/pictures/" + request.args.get('username'))
	# return request.args.get("username")
	
@app.route("/pictures/<username>")
def test(username):
	data = api.getFirst10(username)
	return render_template("viewer.html", images=data["images"], username=username)

@app.route("/full/<username>")
def full(username):
	data = api.getData(username)
	# follows = data["follows"]["count"]
	# followed_by = data["followed_by"]["count"]
	# bio = data["biography"]
	# images = []
	# media = data["media"]["nodes"]
	# for image in media:
		# images.append({"image": image["display_src"], "likes": image["likes"]["count"]})
	# formatted = {"follows": follows, "followed_by": followed_by, "bio": bio, "images": images}
	return str(data)

# This route will show a form to perform an AJAX request
# jQuery is loaded to execute the request and update the
# value of the operation
@app.route('/uploadtest')
def index():
    return render_template('upload.html')

# Route that will process the file upload
@app.route('/upload', methods=['POST'])
def upload():
    # Get the name of the uploaded file
    file = request.files['file']
    # Check if the file is one of the allowed types/extensions
    if file and allowed_file(file.filename):
        # Make the filename safe, remove unsupported chars
        filename = secure_filename(file.filename)
        # Move the file form the temporal folder to
        # the upload folder we setup
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Redirect the user to the uploaded_file route, which
        # will basicaly show on the browser the uploaded file
        image = ClImage(file_obj=open('uploads/' + filename, 'rb'))
        results = []
        classes = []
        probs = []
        users_omega = {}
        images = []
        likes = []
        following = []
        followers = []
        imageinfo = model.predict([image])
        for i in imageinfo['outputs'][0]['data']['concepts']:
            classes.append(i['name'])
            probs.append(i['value'])
        results.append({'result': {'tag': {'classes': classes, 'probs': probs}}})
        tag_pool = []
        for result in results:
            result = result["result"]["tag"]
            tag_pool.extend(result["classes"])
        users_omega['naimmiah08'] = results #needs to be changed for username
        getTags = db.tags_pool.find()
        for tags in getTags:
            print tags['tags']
            tag_pool.extend(tags['tags'])
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
        print images
        print likes
        return redirect(url_for('uploaded_file',
                                filename=filename))
    return "Fuck you"

# This route is expecting a parameter containing the name
# of a file. Then it will locate that file on the upload
# directory and show it on the browser, so if the user uploads
# an image, that image is going to be show after the upload
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)



app.run(host='0.0.0.0', debug=True)

# ZFtpqXvLYJNpw7A8pw3X0RJTFwOycs