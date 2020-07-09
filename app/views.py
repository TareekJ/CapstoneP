"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

import os
from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash, jsonify, _request_ctx_stack
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename

import uuid
import re

## Using JWT
import jwt
from functools import wraps
import base64

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FileField
from wtforms.validators import InputRequired, Email

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])

class RegisterForm(FlaskForm):
    firstname = StringField('Firstname', validators=[InputRequired()])
    lastname = StringField('Lastname', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])

class NewItemForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    description = StringField('Description', validators=[InputRequired()])
    webaddress = StringField('Web Address', validators=[InputRequired()])

class CreateChildForm(FlaskForm):
    child_id = StringField('child_id')
    firstname = StringField('Firstname', validators=[InputRequired()])
    lastname = StringField('Lastname', validators=[InputRequired()])
    age = StringField('Age', validators=[InputRequired()])
    mentorname = StringField('Mentorname', validators=[InputRequired()])
    parentname = StringField('Parentname', validators=[InputRequired()])
    dob = StringField('Dob', validators=[InputRequired()])
    phone = StringField('Phone', validators=[InputRequired()])
    gender = StringField('Gender', validators=[InputRequired()])
    location = StringField('Location', validators=[InputRequired()])
    illness = StringField('Illness', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email()])
    dormnum = StringField('dormnum')
    comments_made = StringField('Comments_made')

class DormRoomForm(FlaskForm):
    dorm_id = StringField('dorm_id', validators=[InputRequired()])
    dorm_gender = StringField('dorm_gender', validators=[InputRequired()])
    dormage_group = StringField('dormage_group', validators=[InputRequired()])
    capacity = StringField('capacity')
    max_capacity = StringField('max_capacity', validators=[InputRequired()])

class SearchChildForm(FlaskForm):
    firstname = StringField('Firstname', validators=[InputRequired()])
    lastname = StringField('Lastname', validators=[InputRequired()])


class CreateDormParentForm(FlaskForm):
    firstname = StringField('firstname', validators=[InputRequired()])
    lastname = StringField('lastname', validators=[InputRequired()])
    phone = StringField('phone', validators=[InputRequired()])
    gender = StringField('gender', validators=[InputRequired()])
    parent_email = StringField('parent_email', validators=[InputRequired(), Email()])
    skills = StringField('skills', validators=[InputRequired()])
    dormnum = StringField('dormnum')

class ShareForm(FlaskForm):
    recipientemail = StringField('Email', validators=[InputRequired(), Email()])
    name = StringField('Name', validators=[InputRequired()])


from . import db

class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<User %r>' % (self.username)


class Child(db.Model):
    child_id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(25))
    lname = db.Column(db.String(30))
    age = db.Column(db.Integer)
    mname = db.Column(db.String(30)) 
    parentname = db.Column(db.String(50))
    dob = db.Column(db.Date)
    phone = db.Column(db.Integer)
    gender = db.Column(db.String(6))
    location = db.Column(db.String(50))
    illness = db.Column(db.String(100))
    email = db.Column(db.String (50))
    dormnum = db.Column(db.Integer)
    comments_made = db.Column(db.String(400))

class Dorm(db.Model):
    dorm_id = db.Column(db.Integer, primary_key=True)
    dorm_gender = db.Column(db.String(6))
    dormage_group = db.Column(db.String(10))
    capacity = db.Column(db.Integer)
    max_capacity = db.Column(db.Integer)

class Comment(db.Model):
    c_id = db.Column(db.Integer, primary_key=True)
    comments_made = db.Column(db.String(400))
    fname = db.Column(db.String(25))
    lname = db.Column(db.String(30))
    
    
class Parent(db.Model):

    fname = db.Column(db.String(25))
    lname= db.Column(db.String(30))
    phone = db.Column(db.Integer)
    gender = db.Column(db.String(6))
    parent_email = db.Column(db.String(35), primary_key=True)
    skills = db.Column((db.String(200)))
    dormnum = db.Column(db.Integer)


###
# Routing for your application.
###

# Create a JWT @requires_auth decorator
# This decorator can be used to denote that a specific route should check
# for a valid JWT token before displaying the contents of that route.
def requires_auth(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    auth = request.headers.get('Authorization', None)
    if not auth:
      return jsonify({'code': 'authorization_header_missing', 'description': 'Authorization header is expected'}), 401

    parts = auth.split()

    if parts[0].lower() != 'bearer':
      return jsonify({'code': 'invalid_header', 'description': 'Authorization header must start with Bearer'}), 401
    elif len(parts) == 1:
      return jsonify({'code': 'invalid_header', 'description': 'Token not found'}), 401
    elif len(parts) > 2:
      return jsonify({'code': 'invalid_header', 'description': 'Authorization header must be Bearer + \s + token'}), 401

    token = parts[1]
    try:
         payload = jwt.decode(token, 'some-secret')

    except jwt.ExpiredSignature:
        return jsonify({'code': 'token_expired', 'description': 'token is expired'}), 401
    except jwt.DecodeError:
        return jsonify({'code': 'token_invalid_signature', 'description': 'Token signature is invalid'}), 401

    g.current_user = user = payload
    return f(*args, **kwargs)

  return decorated

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html', form=None)


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')

@app.route('/view')
def view():
    """Render the website's add page."""
    # retrieve child and dorm parents records from database
    children = Child.query.filter_by().all()
    parents = Parent.query.filter_by().all()
    return render_template('view.html', children=children, parents=parents)

@app.route('/searchchild',methods=["GET","POST"])
def searchchild():
    form = SearchChildForm()
    data =  Child.query.all()
    if request.method == "POST":
        if form.validate_on_submit():
            # generate item id
            id = str(uuid.uuid4().fields[-1])[:8]

            # get data from form
            firstname = form.firstname.data
            lastname = form.lastname.data

            data = Child.query.filter(Child.fname.like(firstname), Child.lname.like(lastname)).all()
            print(data)

            # # all in the search box will return all the tuples
            # if len(datas) == 0 and child == 'all': 
            #     cursor.execute("SELECT fname, lname from child")
            #     conn.commit()
            #     data = cursor.fetchall()
            #     return render_template('searchchild.html', data=data)
    return render_template('searchchild.html', childform=form, children=data)


@app.route('/editparent/<string:parent_email>', methods=["GET","POST"])
def editparent(parent_email):
    form = CreateDormParentForm()
    if request.method == "POST":
        if form.validate_on_submit():
            # generate item id
            id = str(uuid.uuid4().fields[-1])[:8]

            # get data from form
            firstname = form.firstname.data
            lastname = form.lastname.data
            phone = form.phone.data
            gender = form.gender.data
            parent_email = form.parent_email.data
            skills = form.skills.data
            dormnum = form.dormnum.data
            
            # retrieve item from database
            item = db.session.query(Parent).filter(Parent.parent_email==parent_email).first()

            # if the item already exists then flash error message and redirect back to the editparent page
            if item is None:
                flash(''+firstname+' parent does not exist in the table', 'danger')
                return redirect(url_for('editparent', parent_email=parent_email))

            # update parent object
            item.fname=firstname
            item.lname=lastname
            item.phone=phone
            item.gender=gender
            item.parent_email=parent_email
            item.skills=skills
            item.dormnum=dormnum
            print(item.dormnum)
                
            # insert item into Parent
            db.session.commit()

            flash(''+firstname+' was added to your parent table', 'success')

            # redirect user to their view page
            return redirect(url_for("view"))
        else:
            # flash message for failed item addition
            flash('Invalid item data, please try again', 'danger')

            # redirect user to the view page
            return redirect(url_for("view"))

    parent = Parent.query.filter_by(parent_email=parent_email).first()
    if(parent != None):
        form.firstname.data = parent.fname
        form.lastname.data = parent.lname
        form.phone.data = parent.phone
        form.gender.data = parent.gender
        form.parent_email.data = parent.parent_email
        form.skills.data = parent.skills
        form.dormnum.data = parent.dormnum

    return render_template('editparent.html', dormform=form)

@app.route('/add/<int:userid>/', methods=["GET"])
def add(userid):
    
    form = CreateChildForm()
    form2 = CreateDormParentForm()
    """Render the website's add page."""
    # Adds new child or dorm parent to the database
    return render_template('add.html', childform=form, dormform=form2)


@app.route('/child', methods=["POST"])
def child():
    form = CreateChildForm()
    """Render the website's add page."""
    if request.method == "POST":
        if form.validate_on_submit():
            # generate item id
            id = str(uuid.uuid4().fields[-1])[:8]

            # get data from form
            firstname = form.firstname.data
            lastname = form.lastname.data
            age = form.age.data
            mentorname = form.mentorname.data
            parentname = form.parentname.data
            dob = form.age.data
            phone = form.phone.data
            gender = form.gender.data
            location = form.location.data
            illness = form.illness.data
            email = form.email.data
            
            # retrieve item from database
            item = Child.query.filter_by(email=email).first()

            # if the item already exists then flash error message and redirect back to the add page
            if item is not None:
                flash(''+firstname+' already exists in your child table', 'danger')
                return redirect(url_for('add', userid=current_user.get_id()))

            # create child object
            item = Child(
                fname=firstname,
                lname=lastname,
                age=age,
                mname=mentorname,
                parentname=parentname,
                dob=dob,
                phone=phone,
                gender=gender,
                location=location,
                illness=illness,
                email=email)

            # insert item into Child
            db.session.add(item)
            db.session.commit()

            flash(''+firstname+' was added to your child table', 'success')

            # redirect user to their add page
            return redirect(url_for("add", userid=current_user.get_id()))
        else:
            # flash message for failed item addition
            flash('Invalid item data, please try again', 'danger')

            # redirect user to their add page
            return redirect(url_for("add", userid=current_user.get_id()))
        return redirect(url_for("add", userid=current_user.get_id()))


@app.route('/comments/<int:child_id>', methods=["GET","POST"])
def comments(child_id):
    form = CreateChildForm()

    if request.method == "POST":
        if form.validate_on_submit():
            # generate item id
            id = str(uuid.uuid4().fields[-1])[:8]

            # get data from form
            fname = form.firstname.data
            lname = form.lastname.data
            age = form.age.data
            mname = form.mentorname.data
            parentname = form.parentname.data
            dob = form.dob.data
            phone = form.phone.data
            gender = form.gender.data
            location = form.location.data
            illness = form.illness.data
            email = form.email.data
            dormnum = form.dormnum.data
            comments_made = form.comments_made.data
            
            # retrieve item from database
            item = Child.query.filter_by(child_id=child_id).first()
            print(child_id,item)

            # if the item already exists then flash error message and redirect back to the searchchild page
            if item is None:
                flash(''+fname+' Child was not found', 'danger')
                return redirect(url_for('searchchild'))

            # create comment object
            item.child_id = child_id
            item.fname = fname
            item.lname = lname
            item.age = age
            item.mname = mname
            item.parentname = parentname
            item.dob = dob
            item.phone = phone
            item.gender = gender
            item.location = location
            item.illness = illness
            item.email = email
            item.dormnum = dormnum
            item.comments_made = comments_made

            db.session.commit()

            flash('comment for '+fname+' was added to your child table', 'success')

            # redirect user to their add page
            return redirect(url_for("searchchild"))
        else:
            # flash message for failed item addition
            flash('Invalid item data, please try again', 'danger')

            # redirect user to their comments page
            return redirect(url_for("comments", child_id=form.child_id, childform=form))

    item = Child.query.filter_by(child_id=int(child_id)).first()
    print(item)
    if(item != None):
        form.child_id.data = item.child_id
        form.firstname.data = item.fname
        form.lastname.data = item.lname
        form.age.data = item.age
        form.mentorname.data = item.mname
        form.parentname.data = item.parentname
        form.dob.data = item.dob
        form.phone.data = item.phone
        form.gender.data = item.gender
        form.location.data = item.location
        form.illness.data = item.illness
        form.email.data = item.email
        form.dormnum.data = item.dormnum
        form.comments_made.data = item.comments_made
    return render_template("comments.html", childform=form, child_id=child_id)

@app.route("/api/viewRooms", methods=['GET'])
def setrooms():
    assign_rooms()
    dorms = db.session.query(Dorm, Parent).join(Parent, Parent.dormnum == Dorm.dorm_id).all()
    # dorms = Dorm.query.all()
    print(dorms)
    return render_template('viewRooms.html', dorms=dorms)

def getAgeRanges(dorms):  
    ageRanges = []
    # get age ranges from dorm records in database
    for y in range(len(dorms)):
        group = dorms[y].dormage_group.split('-')
        min = int(group[0])
        max = int(group[1])
        ageRanges.append((min,max))
    return ageRanges

def assign_rooms():
    parents = Parent.query.order_by(Parent.gender).all() # get all parents
    children = Child.query.all() # get all children
    dorms = Dorm.query.all() # get dorms

    # update parent and dorm records with dorm ID and gender values
    for x in range(len(parents)):
        parents[x].dormnum = dorms[x].dorm_id # assign dorm number to parent record
        dorms[x].dorm_gender = parents[x].gender # assign parent gender to dorm record


    # organise children into dorms by gender and age
    for child in children:
        # sort the dorms into lowest-capacity-first order so that students are more evenly dispursed
        # dorms = sortDormsByLowestCapacity(dorms)
        ageRanges = getAgeRanges(dorms)
        # print(ageRanges)
        for x in range(len(dorms)):
            currentDorm = dorms[x]
            if child.gender == currentDorm.dorm_gender and child.age >= ageRanges[x][0] and child.age <= ageRanges[x][1] and child.dormnum == None:
                child.dormnum = currentDorm.dorm_id #assign dorm number to child if they meet all the criteria
                if currentDorm.capacity is None: #assign zero to capacity before add operation
                    currentDorm.capacity = 0
                currentDorm.capacity += 1
                break
    
    db.session.commit()

@app.route('/parent', methods=["POST"])
def parent():
    form = CreateDormParentForm()
    """Render the website's add page."""
    if request.method == "POST":
        if form.validate_on_submit():
            # generate item id
            id = str(uuid.uuid4().fields[-1])[:8]

            # get data from form
            firstname = form.firstname.data
            lastname = form.lastname.data
            phone = form.phone.data
            gender = form.gender.data
            parent_email = form.parent_email.data
            skills = form.skills.data
            dormnum = form.dormnum.data
            
            # retrieve item from database
            item = Parent.query.filter_by(parent_email=parent_email).first()
            print (item)

            # if the item already exists then flash error message and redirect back to the wishlist page
            if item is not None:
                flash(''+firstname+' already exists in your add page', 'danger')
                return redirect(url_for('add', userid=current_user.get_id()))

            # create parent object
            item = Parent(
                fname=firstname,
                lname=lastname,
                phone=phone,
                gender=gender,
                parent_email=parent_email,
                skills=skills,
                dormnum=dormnum)

            # insert item into Parent
            db.session.add(item)
            db.session.commit()

            flash(''+firstname+' was added to your child table', 'success')

            # redirect user to their add page
            return redirect(url_for("add", userid=current_user.get_id()))
        else:
            # flash message for failed item addition
            flash('Invalid item data, please try again', 'danger')

            # redirect user to their wishlist page
            return redirect(url_for("add", userid=current_user.get_id()))
    return redirect(url_for("add", userid=current_user.get_id()))



@app.route("/api/users/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST":

        if form.validate_on_submit():
            # get data from form
            email = form.email.data
            password = form.password.data

            # retrieve user from database
            user = UserProfile.query.filter_by(email=email, password=password).first()

            if user is not None:
                # login user
                login_user(user)

                # flash user for successful login
                flash('Logged in as '+current_user.first_name+" "+current_user.last_name, 'success')

                #generate token
                token=generate_token()
                

                # redirect user to their wishlist page
                return redirect(url_for("add", userid=current_user.get_id()))

            # flash user for failed login
            flash('Your email or password is incorrect', 'danger')
            return redirect(url_for("login"))
        else:
            print ("NOT VALIDATED")
            print (form.errors)
            # flash user for incomplete form
            flash('Invalid login data, please try again', 'danger')
    return render_template("login.html", form=form)


## This route is just used to demonstrate a JWT being generated.
@app.route('/token')
def generate_token():
    # Under normal circumstances you would generate this token when a user
    # logs into your web application and you send it back to the frontend
    # where it can be stored in localStorage for any subsequent API requests.
    # generate token
    payload = {'sub': '12345', 'email': current_user.email, 'password': current_user.password}
    token = jwt.encode(payload, 'secret123', algorithm='HS256')
    tokenJSON = jsonify({'error':None, 'token': str(token), 'message':'Token Generated'})
    print(tokenJSON)
    return tokenJSON


@app.route("/api/users/logout")
def logout():
    logout_user()
    flash('Logged out.', 'info')
    return redirect(url_for("login"))


@app.route("/api/users/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if request.method == "POST":
        if form.validate_on_submit():
            # generate userid
            userid = str(uuid.uuid4().fields[-1])[:8]

            # get data from form
            firstname = form.firstname.data
            lastname = form.lastname.data
            email = form.email.data
            password = form.password.data
            

            # retrieve user from database
            user = UserProfile.query.filter_by(email=email, password=password).first()

            # if the user already exists then flash error message and redirect back to the registration page
            if user is not None:
                flash('An account with that email address already exists', 'danger')
                return redirect(url_for('register'))

            # create user object
            user = UserProfile(id=userid,
                               first_name=firstname,
                               last_name=lastname,
                               email=email,
                               password=password)

            # insert user into UserProfile
            db.session.add(user)
            db.session.commit()
            # quit()

            # logout old user
            logout_user()

            # login new user
            login_user(user)

            # flash the user for successful registration
            flash('Registration Successful, Welcome '+current_user.first_name, 'success')

            # redirect user to their add page
            return redirect(url_for("add", userid=current_user.get_id()))

        else:
            print ("NOT VALIDATED")
            print (form.errors)
            flash('Please fill in all fields', 'danger')
            return redirect(url_for('register'))

    return render_template("register.html", form=form)


#

@app.route("/api/users/<string:parent_email>/view/", methods=["GET", "DELETE"])
def removeitem(parent_email):
    if request.method == "DELETE":
        # flash user for successful delete
        flash('Item deleted', 'success')

        # remove item from wishlist
        db.session.delete(Parent.query.filter_by(parent_email=parent_email).first())
        db.session.commit()

        # redirect user to their wishlist page
        return redirect(url_for("view"))
    else:
        # flash user for successful delete
        flash('Item deleted', 'success')

        # remove item from wishlist
        db.session.delete(Parent.query.filter_by(parent_email=parent_email).first())
        db.session.commit()

        return redirect(url_for("view"))

# user_loader callback. This callback is used to reload the user object from
# the user ID stored in the session


@login_manager.user_loader
def load_user(id):
    return UserProfile.query.get(int(id))


@login_manager.unauthorized_handler
def unauthorized_handler():
    flash('Restricted access. Please login to access this page.', 'danger')
    return redirect(url_for('login'))
###
# The functions below should be applicable to all Flask apps.
###




@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8081")
