from catalog_database import Base, Sport, Jersey, User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import (Flask, render_template, request, redirect, url_for,
jsonify, flash, abort, g)

#IMPORTS for Connecting
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

#authorization
from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()


CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']


# Connect to Database and create database session
engine = create_engine('sqlite:///sportscatalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)

#Token based authentication code provided by L. Brown & Udacity's resources
@auth.verify_password
def verify_password(username_or_token, password):
    #Try to see if it's a token first
    user_id = User.verify_auth_token(username_or_token)
    if user_id:
        user = session.query(User).filter_by(id = user_id).one()
    else:
        user = session.query(User).filter_by(username = username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


@app.route('/users', methods = ['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        print "missing arguments"
        abort(400)

    if session.query(User).filter_by(username = username).first() is not None:
        print "existing user"
        user = session.query(User).filter_by(username=username).first()
        return jsonify({'message':'user already exists'}), 200

    user = User(username = username)
    user.hash_password(password)
    session.add(user)
    session.commit()
    return jsonify({ 'username': user.username }), 201


@app.route('/api/users/<int:id>')
def get_user(id):
    user = session.query(User).filter_by(id=id).one()
    if not user:
        abort(400)
    return jsonify({'username': user.username})

@app.route('/api/resource')
@auth.login_required
def get_resource():
    return jsonify({ 'data': 'Hello, %s!' % g.user.username })


# Anti-Forgery state token code provided by L. Brown & Udacity's resources
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
            for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
        credentials = credentials.to_json()
        credentials = json.loads(credentials)

    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials['access_token']
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials['id_token']['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials= login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['credentials'] = credentials
    login_session['access_token'] = access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials['access_token'], 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['provider'] = 'google'
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    user_id = getUserID(login_session['email'])

    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!<br> Email: '
    output += login_session['email']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ''' " style = "width: 300px; height: 300px;
                border-radius: 150px;-webkit-border-radius: 150px;
                -moz-border-radius: 150px;"> '''
    flash("You are now logged in as %s" % login_session['username'])
    print "done!"
    return output


def createUser(login_session):
    ''' This function creates a User in the database along with its
         attributes (Name,Email,Picture) '''

    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    ''' Retrieves an object of the user by giving
        user's id(user_id) as input '''
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    ''' Retrieves the user's id by giving 'email' as input.'''
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# JSON APIs
@app.route('/sport/<int:sport_id>/catalog/JSON')
def jerseyCatalogJSON(sport_id):
    sport = session.query(Sport).filter_by(id=sport_id).one()
    jerseys = session.query(Jersey).filter_by(sport_id=sport_id).all()
    return jsonify(Jerseys=[i.serialize for i in jerseys])


@app.route('/sport/<int:sport_id>/catalog/<int:catalog_id>/JSON')
def jerseyJSON(sport_id, catalog_id):
    Jersey_Item = session.query(Jersey).filter_by(id=catalog_id).one()
    return jsonify(Jersey_Item=Jersey_Item.serialize)


@app.route('/sport/JSON')
def sportsJSON():
    sports = session.query(Sport).all()
    return jsonify(sports=[i.serialize for i in sports])


# View all sports
@app.route('/')
@app.route('/sports')
def showSports():
    # return "This page will return all the sports!"
    sports = session.query(Sport).all()
    return render_template('sports.html', sports=sports)


# View all the jerseys of a specific sport
@app.route('/sport/<int:sport_id>/catalog')
@app.route('/sport/<int:sport_id>')
def showJersey(sport_id):
    sport = session.query(Sport).filter_by(id=sport_id).one()
    jerseys = session.query(Jersey).filter_by(sport_id=sport_id).all()
    return render_template('jerseyList.html', sport=sport, jerseys=jerseys)


# Create a new jersey item
@app.route('/sport/<int:sport_id>/catalog/new',methods=['GET', 'POST'])
def newJerseyItem(sport_id):
    # User must be logged in order to create a new item
    if 'user_id' not in login_session:
        return redirect('/error/authentication')

    if request.method == 'POST':
        newJersey = Jersey(name=request.form['name'],
                    description=request.form['description'],
                    price=request.form['price'], sport_id=sport_id,
                    user_id=login_session['user_id'])
        session.add(newJersey)
        session.commit()
        return redirect(url_for('showJersey', sport_id=sport_id))
    else:
        return render_template('newJersey.html', sport_id=sport_id)


# Edit jersey items
@app.route('/sport/<int:sport_id>/catalog/<int:catalog_id>/edit',
           methods=['GET', 'POST'])
def editJerseyItem(sport_id, catalog_id):
    # User at the very least must be logged in
    if 'user_id' not in login_session:
        return redirect('/error/authentication')
    editedJersey = session.query(Jersey).filter_by(id=catalog_id).one()

    # User must also be authorized to edit this item
    if login_session['user_id'] != editedJersey.user_id:
        return redirect('/error/authorization')

    if request.method == 'POST':
        if request.form['name']:
            editedJersey.name = request.form['name']
        if request.form['description']:
            editedJersey.description = request.form['description']
        if request.form['price']:
            editedJersey.price = request.form['price']
        session.add(editedJersey)
        session.commit()
        return redirect(url_for('showJersey', sport_id=sport_id))
    else:
        return render_template('editJersey.html', sport_id=sport_id,
                                catalog_id=catalog_id, item=editedJersey)


# Delete jersey items
@app.route('/sport/<int:sport_id>/catalog/<int:catalog_id>/delete',
           methods=['GET', 'POST'])
def deleteJerseyItem(sport_id, catalog_id):
    # User at the very least must be logged in
    if 'user_id' not in login_session:
        return redirect('/error/authentication')
    jerseyToDelete = session.query(Jersey).filter_by(id=catalog_id).one()

    # User must also be authorized to delete this item
    if login_session['user_id'] != jerseyToDelete.user_id:
        return redirect('/error/authorization')

    if request.method == 'POST':
        session.delete(jerseyToDelete)
        session.commit()
        return redirect(url_for('showJersey', sport_id=sport_id))
    else:
        return render_template('deleteJersey.html', sport_id=sport_id,
                                catalog_id=catalog_id, item=jerseyToDelete)


# Error page when user is not logged in
@app.route('/error/authentication')
def errorPage():
    return render_template('errorAuthentication.html')

# Error page when user is not authorized to edit/delete items
@app.route('/error/authorization')
def errorPage2():
    return render_template('errorAuthorization.html')

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
