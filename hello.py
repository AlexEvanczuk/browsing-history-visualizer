import os, requests, urlparse, psycopg2
from flask import Flask, render_template, send_from_directory, request, jsonify, json
from flask.ext.sqlalchemy import SQLAlchemy
from collections import OrderedDict

app = Flask(__name__)

urlparse.uses_netloc.append("postgres")

# Hardcoded database URL
databaseURL = "postgres://tijkqeozlvrknb:YnxZpXG4YeL44bNyky4CLlCA56@ec2-54-197-237-171.compute-1.amazonaws.com:5432/d8lbdq4dm2r9ia"
#url = urlparse.urlparse(os.environ["DATABASE_URL"])
url = urlparse.urlparse(databaseURL)

# Uncomment these lines to find connection.  Can also use 
# heroku pg:credentials heroku_postgresql_brown_url or heroku config
debug = '''
database=url.path[1:],
user=url.username,
password=url.password,
host=url.hostname,
port=url.port
print(database)
print(user)
print(password)
print(host)
print(port)
#print("Connection is:") 
#print("psql -h " + url.hostname + " -p " + str(url.port) + " -u " + url.path[1:])
'''

# Connect to the psql database using the url connection string
conn = psycopg2.connect(
database=url.path[1:],
user=url.username,
password=url.password,
host=url.hostname,
port=url.port
)

print("Entered App")
# Handle post requests from the chrome extension by pulling the url args
# and inserting the values into the psql database
@app.route('/api', methods = ['POST'])
def handle_post():

	print('Enter Handle Post')
	site1 = request.form.get('site1');
	time = request.form.get('time');
	site2 = request.form.get('site2');
	print(site1, time, site2)
	cur = conn.cursor()
	cur.execute("INSERT INTO connections VALUES (%s, %s, %s)",  (site1, time, site2))
	conn.commit();
	cur.close()
	
	# Disable chrome throttling (optional)
	uncommentToDisable = '''
	response = make_response('Completed Update')
	response.headers['X-Chrome-Exponential-Throttling'] = 'disable'
	return response '''
	return 'Completed Update'
	

@app.route('/hello')
def hello_world():
	return 'Hello World!'

@app.route('/')
def index():
	print("Entered Index Page")
	return render_template('index.html')
	#return 'Index Page'

# This method returns all connection data and turns it into a form necessary for 
# D3 force-directed graph
@app.route('/yourdata.json')
def yourdata():
	cur = conn.cursor()
	cur.execute("SELECT * FROM connections;")
	result = cur.fetchall()

	# Create nodes as a list of dictionaries 
	from itertools import groupby
	from collections import OrderedDict
	nodes = OrderedDict()
	data = sorted(result, key=lambda x: x[0])
	for key, group in groupby(data, lambda x: x[0]):
		key = urlparse.urlparse(key).netloc
		timeSum = sum([ele[1] for ele in group])
		nodes[key] = timeSum
	
	# If the site2 is not in the nodelist, add it with a default time value of 1000
	for key, group in groupby(result, lambda x: x[2]):
		key = urlparse.urlparse(key).netloc
		if key not in nodes:
			nodes[key] = 1000

	# Create links as a list of dictionaries 
	edges = []
	for (site1, time, site2) in result:
		site1 = urlparse.urlparse(site1).netloc
		site2 = urlparse.urlparse(site2).netloc

		edge = {"source": nodes.keys().index(site1), "target":nodes.keys().index(site2), "value": nodes[site1]}
		edges.append(edge)

	# Refactor the nodes dictionary as a list of dictionaries with naemd fields
	nodes = [{"name": n, "group": nodes[n]} for n in nodes]

	# Create dataset
	dataset = {}
	dataset['nodes'] = nodes
	dataset['links'] = edges

	dataset = json.dumps(dataset)
	cur.close()
	return(dataset)

# TODO: Complete
@app.route('/user/<int:username>')
def show_user_profile(username):
	# show the user profile for this user id (integer) if user is published
	return 'User %s' % username

# TODO: Debug = false
if __name__ == '__main__':
	app.run(debug=True)

# Close connection to database??
