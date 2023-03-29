# imports
from flask import Flask, request, make_response, render_template
from sqlalchemy import text
#from flask_sqlalchemy import sqlalchemy as sql
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, insert
from sqlalchemy import create_engine
# initializing Flask app
app = Flask(__name__)

# Google Cloud SQL (change this accordingly)
PASSWORD ="tulip"
PUBLIC_IP_ADDRESS ="35.204.202.19"
DBNAME ="guest-book-database"
PROJECT_ID ="raniamoh-playground"
INSTANCE_NAME ="guest-book"

# configuration
#app.config["SECRET_KEY"] = "yoursecretkey"
#app.config["SQLALCHEMY_DATABASE_URI"]= f"mysql + mysqldb://postgres:{PASSWORD}@{PUBLIC_IP_ADDRESS}/{DBNAME}?
#unix_socket =/cloudsql/{PROJECT_ID}:{INSTANCE_NAME}"
#app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= True
db_string = f"postgresql://guest-user:{PASSWORD}@{PUBLIC_IP_ADDRESS}:5432/{DBNAME}"

db = create_engine(db_string)
Base = declarative_base()

# User ORM for SQLAlchemy
class Users(Base):
	__tablename__ = 'users'
	id = Column(Integer, primary_key = True, nullable = False, autoincrement=True)
	guest_name = Column(String(50), nullable = False)
	content = Column(String(50), nullable = False, unique = True)
Base.metadata.create_all(db)

@app.route('/guestbook/sign', methods =['POST'])
def add():
	# getting name and email
	guest_name = request.form.get('guest_name')
	content = request.form.get('content')
	with db.connect() as con:
		users =  con.execute(text(f"SELECT * FROM users WHERE guest_name = '{guest_name}'"))
  
	print(users.fetchone())
	row = users.fetchone()
	if row == None:
		# creating Users object
		print("There are no results for this query")
		user = Users(
			guest_name = guest_name,
			content = content
		)
		#stmt = (insert("users").values(guest_name = guest_name, content = content))
		with db.connect() as con:
			con.execute(text(f"INSERT INTO users (guest_name, content) VALUES ('{guest_name}', '{content}')"))
			con.commit()
		# adding the fields to users table
		#db.commit()
		# response
		responseObject = {
			'status' : 'success',
			'message': 'Successfully registered.'
		}

		return make_response(responseObject, 200)
		
	else:
		# if user already exists then send status as fail
		responseObject = {
			'status' : 'fail',
			'message': 'User already exists !!'
		}

		return make_response(responseObject, 403)

@app.route('/guestbook/view')
def view():
	
	# fetches all the users
	with db.connect() as con:
		users =  con.execute(text("SELECT * FROM users"))
	responseUsers = list()
	for row in users:
		print (row)
		responseUsers.append({
			"guest_name" : row[1],
			"content": row[2]
		})
	print (responseUsers)
	return render_template("index.html", rows=responseUsers)


if __name__ == "__main__":
	# serving the app directly
	app.run()
