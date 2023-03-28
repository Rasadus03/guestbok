# imports
from flask import Flask, request, make_response
from flask_sqlalchemy import SQLAlchemy

# initializing Flask app
app = Flask(__name__)

# Google Cloud SQL (change this accordingly)
PASSWORD ="cGFzc3dvcmQ="
PUBLIC_IP_ADDRESS ="35.204.202.19"
DBNAME ="guest-book-database"
PROJECT_ID ="raniamoh-playground"
INSTANCE_NAME ="guest-book"

# configuration
#app.config["SECRET_KEY"] = "yoursecretkey"
#app.config["SQLALCHEMY_DATABASE_URI"]= f"mysql + mysqldb://postgres:{PASSWORD}@{PUBLIC_IP_ADDRESS}/{DBNAME}?
#unix_socket =/cloudsql/{PROJECT_ID}:{INSTANCE_NAME}"
#app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= True
db_string = f"postgres://admin:{PASSWORD}@{PUBLIC_IP_ADDRESS}:15813/{DBNAME}"

db = SQLAlchemy(db_string)

# User ORM for SQLAlchemy
class Users(db.Model):
	id = db.Column(db.Integer, primary_key = True, nullable = False)
	guest_name = db.Column(db.String(50), nullable = False)
	content = db.Column(db.String(50), nullable = False, unique = True)

@app.route('/sign', methods =['POST'])
def add():
	# getting name and email
	guest_name = request.form.get('guest_name')
	content = request.form.get('content')

	# checking if user already exists
	user = Users.query.filter_by(guest_name = guest_name).first()

	if not user:
		try:
			# creating Users object
			user = Users(
				guest_name = guest_name,
				content = content
			)
			# adding the fields to users table
			db.session.add(user)
			db.session.commit()
			# response
			responseObject = {
				'status' : 'success',
				'message': 'Successfully registered.'
			}

			return make_response(responseObject, 200)
		except:
			responseObject = {
				'status' : 'fail',
				'message': 'Some error occurred !!'
			}

			return make_response(responseObject, 400)
		
	else:
		# if user already exists then send status as fail
		responseObject = {
			'status' : 'fail',
			'message': 'User already exists !!'
		}

		return make_response(responseObject, 403)

@app.route('/view')
def view():
	# fetches all the users
	users = Users.query.all()
	# response list consisting user details
	response = list()

	for user in users:
		response.append({
			"guest_name" : user.guest_name,
			"content": user.content
		})

	return make_response({
		'status' : 'success',
		'message': response
	}, 200)


if __name__ == "__main__":
	# serving the app directly
	app.run()
