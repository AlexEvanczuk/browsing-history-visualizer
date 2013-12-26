import os, requests, urlparse, psycopg2
from flask import Flask, render_template, send_from_directory
#from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
#db = SQLAlchemy(app)

urlparse.uses_netloc.append("postgres")
databaseURL = "postgres://tijkqeozlvrknb:YnxZpXG4YeL44bNyky4CLlCA56@ec2-54-197-237-171.compute-1.amazonaws.com:5432/d8lbdq4dm2r9ia"
#url = urlparse.urlparse(os.environ["DATABASE_URL"])
url = urlparse.urlparse(databaseURL)

conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)


#print("host: " + url.hostname)
#print("port: " + str(url.port))
#print("database: " + url.path[1:])
#print("Connection is:") 
#print("psql -h " + url.hostname + " -p " + str(url.port) + " -u " + url.path[1:])

@app.route('/api', methods = ['POST'])
def handle_post():
	cur = conn.cursor()
	site1 = requests.get['site1']
	time = requests.get['time']
	site2 = requests.get['site2']
	cur.execute("INSERT INTO connections VALUES (%s, %s, %s)",  site1, time, site2)
	cur.execute("SELECT * FROM connections;")
	conn.commit();
	for record in cur:
		print(record);
	conn.close()
	cur.close()

@app.route('/hello')
def hello_world():
	return 'Hello World!'

@app.route('/')
def index():
	cur = conn.cursor()
	#cur.execute("INSERT INTO users VALUES 1;")
	cur.execute("INSERT INTO connections VALUES (%s, %s, %s)",  ("amazon.com", 1500, "facebook.com"))
	cur.execute("SELECT * FROM connections;")
	conn.commit();
	for record in cur:
		print(record);
	conn.close()
	cur.close()
	return render_template('index.html')
	#return 'Index Page'

@app.route('/user/<username>')
def show_user_profile(username):
	# show the user profile for that user
	return 'User %s' % username

@app.route('/post/<int:post_id>')
def show_post(post_id):
	# show the post with the given id, the id is an integer
	return 'Post %d' % post_id

if __name__ == '__main__':
	app.run(debug=True)
