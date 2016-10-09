import json
import requests

def search(query):
	link = "https://www.instagram.com/web/search/topsearch/?context=blended&query=" + query
	response = requests.get(link)
	return response.json()

def getId(username):
	user = search(username)
	user = user["users"][0]
	return user["user"]["pk"]

def getMedia(username):
	link = "https://www.instagram.com/" + username + "/media/"
	response = requests.get(link)
	return response.json()
	
def getData(username):
	id = getId(username)
	url = "https://www.instagram.com/" + username + "/?__a=1"
	payload = {}
	cookie = 'Cookie: mid=V_k_AQAEAAGTrrfINeOjN593Fx7o; ig_pr=1; ig_vw=1366; s_network=; csrftoken=polyAG8uxopCeqxYvegL7X7nwZWH6byg; sessionid=IGSC71d917d416b5ec5f43a6addb35b65f788f10cb9f83acfba7073330dc911afc0f:V5kBxMVCXlwHpsP9kPbazoySLU5kpxdM:{"_token_ver":2,"_auth_user_id":1819659594,"_token":"1819659594:t9SjDJyMYnkLvGg6qvNpkGJw48YttzER:d33617f4c1d8445174ac40908d001c82092de0c8c06bf1105a1dc1c86cd618c2","asns":{"192.76.177.124":12,"time":1475953872},"_auth_user_backend":"accounts.backends.CaseInsensitiveModelBackend","last_refreshed":1475953872.117688,"_platform":4,"_auth_user_hash":""}; ds_user_id=' + str(id)
	headers = {
		"Host": "www.instagram.com",
		"Accept": "*/*",
		"Accept-Language": "en-US,en;q=0.5",
		"X-Requested-With": "XMLHttpRequest",
		"Referer": "https://www.instagram.com/" + username + "/" ,
		"X-Instagram-AJAX": "1",
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0",
		"Cookie": cookie,
        "origin": "https://www.instagram.com",
        "x-csrftoken": "GI3edEcZqeX74jAt0JRva80HQoMWvvfY",
        "x-instagram-ajax": "1",
        "authority": "www.instagram.com"
	}
	response = requests.get(url, headers=headers)
	response = response.json()["user"]
	return response

def getFollowers(username, followcount):
    data = getData(username)
    id = str(getId(username))
    link = "https://www.instagram.com/query/"
    cookie = 'cookie: mid=V-wD1QAEAAEW44x_1M8EDNiHRXMh; fbm_124024574287414=base_domain=.instagram.com; sessionid=IGSC37ca9919ba5877bf7a73726f1ce984a982bf9814dc91ecbcfe072743774f4b03%3AnxWkpGQMWsIY6Pr0H8LJEEHfRR94kxuC%3A%7B%22_token_ver%22%3A2%2C%22_auth_user_id%22%3A1819659594%2C%22_token%22%3A%221819659594%3AzHLJ7vJH0zDI9tLznaiAT57uHcQ4WUEa%3Adac02cae7220ca392d6063d1c9a9c41f37ab73bcaac97139887b177f638fce49%22%2C%22asns%22%3A%7B%22time%22%3A1475990034%2C%22192.76.177.124%22%3A12%7D%2C%22_auth_user_backend%22%3A%22accounts.backends.CaseInsensitiveModelBackend%22%2C%22last_refreshed%22%3A1475999150.203311%2C%22_platform%22%3A4%2C%22_auth_user_hash%22%3A%22%22%7D; ig_pr=2; ig_vw=1818; s_network=; fbsr_124024574287414=O6xNwnfFavbRiB9KlBVQ0TszsrfggcQ7KaA2_ujWX_g.eyJhbGdvcml0aG0iOiJITUFDLVNIQTI1NiIsImNvZGUiOiJBUURjWUpXdVQ1UGZTUnRUeng4Rjh0eU9JWjVheVZkdW5rSnd4bVd4MXl3aklMVG5yUkl5VEYyTDdSQTFxMEFjUFlaNEtZbzBoS2dvbXhIbFViaGRBTWctQnI1ZVlVRmVuNVBlQWI3VjdHMlk2MmhZbVhBTnFUdWZFbHZrcHp4eDFKbmg3d1NzTlpva0Uwb1liOUotZ0w3ZkZWWjZIQnd6VmdFNU9OMFdhWTh0ajFPdlRlc29IVENwaTFVbk40YUlDNVp5ajROZlZXZWpLMUFPTU9WZU1xS1FQNUc1LTIzSlF3UVhDOGVIeVNyTjZTOEVpdjhWVnFYR20zVU15N1Qxb3VoRmYyNHBUcXd2WWxGWENiVEptb3AxSTBpc0tCM0EzVHotLU1FZkpBWXNiQ2V3czctYTJGRTJSc0d6MGRBX1ZFc3NjcEpwdjJ5WWpXZ0VoeTQ0bVFwRyIsImlzc3VlZF9hdCI6MTQ3NTk5OTIxMiwidXNlcl9pZCI6IjE3MDA4NTA5OTUifQ; csrftoken=RFWzDB2Sr4B9yt6YTfwlhitEJl9bQum8; ds_user_id=' + id
    payload = {}
    headers = {
            "Host": "www.instagram.com",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.5",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "https://www.instagram.com/" + username + "/" ,
            "X-Instagram-AJAX": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0",
            "Cookie": cookie,
            "origin": "https://www.instagram.com",
            "x-csrftoken": "RFWzDB2Sr4B9yt6YTfwlhitEJl9bQum8",
            "x-instagram-ajax": "1",
            "authority": "www.instagram.com"
        }
    query = 'q=ig_user('+id+')+%7B%0A++followed_by.first('+str(followcount)+')+%7B%0A++++count%2C%0A++++page_info+%7B%0A++++++end_cursor%2C%0A++++++has_next_page%0A++++%7D%2C%0A++++nodes+%7B%0A++++++id%2C%0A++++++is_verified%2C%0A++++++followed_by_viewer%2C%0A++++++requested_by_viewer%2C%0A++++++full_name%2C%0A++++++profile_pic_url%2C%0A++++++username%0A++++%7D%0A++%7D%0A%7D%0A&ref=relationships%3A%3Afollow_list&query_id=17851938028087704'
    response = requests.post(link, data=payload)
    return response

def getPicturesRecursive(username, id, has_next, end, pictures):
	if has_next:
		url = 'https://www.instagram.com/query/'
		cookie = 'cookie: mid=V-wD1QAEAAEW44x_1M8EDNiHRXMh; fbm_124024574287414=base_domain=.instagram.com; sessionid=IGSC7df09cfe996c0185701b1f1742bc462cbda800512a3f254a7544184ac2be0b13:VMELBQ9EzqD53Ta3rsiqONr2AEvgPtFk:{"asns":{"192.76.177.124":12,"time":1475990034}}; ig_pr=2; ig_vw=1818; fbsr_124024574287414=Viaa6VIyPzTQ4wG4_zr46orA6t92xKL7miP9octrw-Q.eyJhbGdvcml0aG0iOiJITUFDLVNIQTI1NiIsImNvZGUiOiJBUUNOb0RaTlBFWmk2Nnl0cjMyZmliazlwMWV6TkJOTHJFclJUQS15a3o0VU94NUU5YkMyZVA5OFFxelZ4M29RSTN3YW9sY1drTUsxbUlWOVp5SGZpUWUyVHZiOVExRWEtcU5jTjNVOFhkWkp1QnBOY0pwXzBDVzFBbmhySFVCb2J2S2xxbDVidjI1R1drZGo0d3ptY21tWnpPT0d2SUVjRHVUZEhJLXlWZGdUSUJ2U0xqM01NM2tjNGx0VzI0d1hqSnBtemxSN0VocWc4cENpR1VfSWFkTHBsQlVRT3Fiekp1WlRTd0RNQmpOZXhJUjhidHVLbE1VWHhTRjMwanVlX1pCejhkRWNla1MwWXFydzA2dnNQWFhxdUlQNlA4Tkt3cVY3OGFCU0tDWWFPVXlucFFnOU9sdUFKRHVidmtnZGN6Tk44OGg3LUN0dEM3emRMRUNBWkFqOCIsImlzc3VlZF9hdCI6MTQ3NTk5MDM4MywidXNlcl9pZCI6IjE3MDA4NTA5OTUifQ; s_network=; csrftoken=GI3edEcZqeX74jAt0JRva80HQoMWvvfY'
		headers = {
			"Host": "www.instagram.com",
			"Accept": "*/*",
			"Accept-Language": "en-US,en;q=0.5",
			"X-Requested-With": "XMLHttpRequest",
			"Referer": "https://www.instagram.com/" + username + "/" ,
			"X-Instagram-AJAX": "1",
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0",
			"Cookie": cookie,
			"origin": "https://www.instagram.com",
			"x-csrftoken": "GI3edEcZqeX74jAt0JRva80HQoMWvvfY",
			"x-instagram-ajax": "1",
			"authority": "www.instagram.com"
		}
		query = 'q=ig_user('+id+')+%7B+media.after('+end+'%2C+12)+%7B%0A++count%2C%0A++nodes+%7B%0A++++caption%2C%0A++++code%2C%0A++++comments+%7B%0A++++++count%0A++++%7D%2C%0A++++comments_disabled%2C%0A++++date%2C%0A++++dimensions+%7B%0A++++++height%2C%0A++++++width%0A++++%7D%2C%0A++++display_src%2C%0A++++id%2C%0A++++is_video%2C%0A++++likes+%7B%0A++++++count%0A++++%7D%2C%0A++++owner+%7B%0A++++++id%0A++++%7D%2C%0A++++thumbnail_src%2C%0A++++video_views%0A++%7D%2C%0A++page_info%0A%7D%0A+%7D&ref=users%3A%3Ashow&query_id=17842962958175392'
		response = requests.get(url + '?' + query, headers=headers)
		data = response.json()
		media = data["media"]
		page_info = media["page_info"]
		pictures.extend(media["nodes"])
		
		return getPicturesRecursive(username, id, page_info["has_next_page"], page_info["end_cursor"], pictures)
	else:
		return pictures

def getPictures(username):
	data = getData(username)
	id = str(getId(username))
	media = data["media"]
	page_info = media["page_info"]
	pictures = media["nodes"]
	return getPicturesRecursive(username, id, page_info["has_next_page"], page_info["end_cursor"], pictures)

def getFirst10(username):
	data = getData(username)
	if data["is_private"]:
		return "User is private"
	else:
		output = {"name": data["full_name"]}
		media = data["media"]["nodes"]
		images = []
		for image in media:
			images.append({"image": image["display_src"], "likes": image["likes"]["count"]})
		output["images"] = images
		return output

# data = getData("naimmiah08")
# follows = data["follows"]["count"]
# followers = data["followed_by"]["count"]
# print follows, followers