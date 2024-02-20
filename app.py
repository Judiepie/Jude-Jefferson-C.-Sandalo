from flask import Flask,render_template,request,redirect,url_for,flash,session
from dbhelper import *

app = Flask(__name__)
app.secret_key = "!@#$%"
head:list = ['idno','lastname','firstname','course','level','action']
	
	
        
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response
	
@app.route("/logout")
def logout()->None:
	if "username" in session:
		session.pop("username")
		flash("Logged Out")
	return render_template("index.html",title="JS BOOKS")
	


@app.route("/savestudent",methods=['POST'])
def savestudent()->None:
	flag:str = request.form['flag']
	print(flag)
	if "username" in session:
		idno:str = request.form['idno']
		lastname:str = request.form['lastname']
		firstname:str = request.form['firstname']
		course:str = request.form['course']
		level:str = request.form['level']
		if flag == "False":
			ok:bool = addrecord('student',idno=idno,lastname=lastname,firstname=firstname,course=course,level=level)
			if ok:
				flash("New Student Added")
			return redirect("home")
		else:
			ok:bool = updaterecord('student',idno=idno,lastname=lastname,firstname=firstname,course=course,level=level)
			if ok:
				flash("Student Updated")
			return redirect("home")
	else:
		flash("Login Properly")
		return redirect(url_for("login"))
		

	
	
@app.route("/deletestudent/<idno>")
def deletestudent(idno)->None:
	if "username" in session:
		ok:bool = deleterecord('student',idno=idno)
		if ok:
			flash("Student Deleted")
	#return render_template("home.html",title="home",data=slist,header=head)		
	return redirect(url_for("home"))	
	
@app.route("/home")
def home()->None:
	if "username" in session:
		slist = getall('student')
		return render_template("home.html",title="home",data=slist,header=head)
	else:
		flash("Login Properly")
		return render_template("index.html")

@app.route("/login",methods=['POST','GET'])
def login()->None:
	if request.method == "POST":
		uname:str = request.form['username']
		pword:str = request.form['password']
		#set a static user validation
		user:list = userlogin('user',username=uname,password=pword)
		print(dict(user[0]))
		if len(user)>0:
			session['username'] = uname
			return redirect(url_for("home"))
		else:
			flash("Invalid User")
			return render_template("login.html",title="JS BOOKS")
	else:
		return render_template("login.html",title="JS BOOKS")


@app.route("/")
def main()->None:
	return render_template("index.html",title="JS BOOKS")
	
if __name__=="__main__":
	app.run(host="0.0.0.0",debug=True)
	
	
	