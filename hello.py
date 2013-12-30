import os, requests, urlparse, psycopg2
from flask import Flask, render_template, send_from_directory, request
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)

urlparse.uses_netloc.append("postgres")
# Hardcoded database URL
databaseURL = "postgres://tijkqeozlvrknb:YnxZpXG4YeL44bNyky4CLlCA56@ec2-54-197-237-171.compute-1.amazonaws.com:5432/d8lbdq4dm2r9ia"
#app.config['SQLALCHEMY_DATABASE_URI'] = databaseURL
#db = SQLAlchemy(app)

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

#print(db)
# Connect to the psql database using the url connection string
conn = psycopg2.connect(
database=url.path[1:],
user=url.username,
password=url.password,
host=url.hostname,
port=url.port
)
#
#try: 
#except Exception, e: 
#d	print "Exception raised: %s" % e

print("entered app")
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
	print("index")
	cur = conn.cursor()
	cur.execute("SELECT * FROM connections;")
	result = cur.fetchall()
	print(result)
	cur.close()
	return render_template('index.html')
	#return 'Index Page'

# TODO: Complete
@app.route('/user/<int:username>')
def show_user_profile(username):
	# show the user profile for this user id (integer) if user is published
	return 'User %s' % username

# TODO: Debug = false
if __name__ == '__main__':
	app.run(debug=True)

# Close connection to database??
