from flask import Flask
from flask import request
import random, base64, os, time
app = Flask(__name__)

# content for reading html files, flask is wonky with the built-ins
# on different platforms for some reason
# @TODO fix cross platform issues
def get_html(filename):
	file = open(filename, 'r')
	data = file.read()
	file.close()
	return data

# base64 encode some data for query strings
def encode(raw_string):
	string_bytes = str.encode(raw_string)
	base_64_string = base64.b64encode(string_bytes)
	encoded_string = base_64_string.decode().replace("==", "")
	return encoded_string

def decode(encoded_string):
	byte_string = base64.b64decode(encoded_string+"==")
	return byte_string.decode()

# generate some random ballot results based questions.txt
def generate_results(ballot):
	# get row template
	row_template = get_html("ballot_row_template.html")
	
	# read and shuffle questions
	file = open("questions.txt", 'r')
	questions = file.readlines()
	file.close()
	random.shuffle(questions)
	
	question_num = random.randint(30, len(questions))
	for x in range(0, question_num):
		# add a row to our ballot
		row_copy = row_template
		
		# add question
		row_copy = row_copy.replace("question", questions[x])
		# add voter count
		voters = str(random.randint(834, 84598))
		row_copy = row_copy.replace("voter_count", voters)
		# add percent complete
		complete = str(random.randint(1, 101))
		row_copy = row_copy.replace("percent_complete", complete)
		# add authentication required
		req = "Yes"
		if random.randint(0, 100) > 50:
			req = "No"
		row_copy = row_copy.replace("authentication_required", req)
		# add results link
		base_64_question = encode(questions[x])
		results_link = "/ballot_results?question="+base_64_question+"&complete="+complete+"&voters="+voters
		button_template = get_html("button_template.html")
		button_template = button_template.replace("LINK_STRING", results_link)
		row_copy = row_copy.replace("results_link", button_template)
		# add voting link
		vote_template = get_html("vote_button_template.html")
		vote_link = "/vote?question="+base_64_question
		vote_template = vote_template.replace("LINK_STRING", vote_link)
		row_copy = row_copy.replace("vote_link", vote_template)
		
		# add row to ballot
		ballot = ballot.replace("<!-- End of ballot. -->", row_copy)
	return ballot

@app.route('/')
def index():
	data = get_html("index.html")
	return data

@app.route('/login_voter')
def login_voter():
	return get_html("login.html")

@app.route('/login_admin')
def login_admin():
	return get_html("login_admin.html")

@app.route('/validate_identity')
def validate():
	return 'Identity page!'
	
@app.route('/create_ballot')
def create_ballot():
	page = get_html("create_ballot.html")
	return page

@app.route('/vote', methods=['GET', 'POST'])
def vote():
	# get question
	question = decode(request.args.get("question"))
	
	vote_template = get_html("cast_vote.html")
	
	vote_template = vote_template.replace("QUESTION_STRING", question)
	
	return vote_template

@app.route('/view_ballots')
def view_ballots():
	# get the ballot template
	ballot_page = get_html("ballot_list_template.html")
	
	# generate some random ballots, along with results
	ballot_page = generate_results(ballot_page)
	
	return ballot_page

@app.route('/ballot_results', methods=['GET', 'POST'])
def ballot_results():
	# get question
	question = decode(request.args.get("question"))
	# get percent complete
	complete = request.args.get("complete")
	# get number of voters
	voters = request.args.get("voters")
	
	# generate some results
	available_votes = int((float(100.0-float(complete)) / 100.0) * int(voters))
	no_response = int((float(complete) / 100.0) * int(voters))
	yes = random.randint(0, available_votes)
	available_votes -= yes
	no = random.randint(0, available_votes)
	available_votes -= no
	maybe = available_votes
	
	# clean up old images
	os.system("del static\\chart*.png")
	
	# generate chart and serve on html page
	num = random.randint(500, 50000)
	filename = "static\\chart_"+str(num)+".png"
	os.system("python generate_pie.py \"Yes,No,Unsure,No Response\" \""+str(yes)+","+str(no)+","+str(maybe)+","+str(no_response)+"\" "+filename+" \""+question+"\"")
	
	ballot_page = "<img src=\""+filename+"\" alt=\"Ballot Results\" width=\"640\" height=\"480\">"
	return ballot_page