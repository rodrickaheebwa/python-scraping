# Method 2
# Inspection

# https://www.zenrows.com/blog/web-scraping-login-python

import requests 
from bs4 import BeautifulSoup 
 
login = "Your Username Here" 
password = "Your Password Here" 
login_url = "https://github.com/session" 
repos_url = "https://github.com/" + login + "/?tab=repositories" 
 
with requests.session() as s: 
	req = s.get(login_url).text 
	html = BeautifulSoup(req,"html.parser") 
	token = html.find("input", {"name": "authenticity_token"}).attrs["value"] 
	time = html.find("input", {"name": "timestamp"}).attrs["value"] 
	timeSecret = html.find("input", {"name": "timestamp_secret"}).attrs["value"] 
 
	payload = { 
		"authenticity_token": token, 
		"login": login, 
		"password": password, 
		"timestamp": time, 
		"timestamp_secret": timeSecret 
	} 
	res =s.post(login_url, data=payload) 
 
	r = s.get(repos_url) 
	soup = BeautifulSoup (r.content, "html.parser") 
	usernameDiv = soup.find("span", class_="p-nickname vcard-username d-block") 
	print("Username: " + usernameDiv.getText()) 
 
	repos = soup.find_all("h3", class_="wb-break-all") 
	for r in repos: 
		repoName = r.find("a").getText() 
		print("Repository Name: " + repoName)


# check for the input fields
# check for the action route/url if it's there