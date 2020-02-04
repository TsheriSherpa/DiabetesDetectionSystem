# Python modules
import os, logging 

# Flask modules
from flask               import render_template, request, url_for, redirect, send_from_directory
from flask_login         import login_user, logout_user, current_user, login_required
from werkzeug.exceptions import HTTPException, NotFound, abort

# App modules
from app        import app, lm, db, bc
from app.models import User
from app.forms  import LoginForm, RegisterForm, ProfileUpdateForm, DetectDiabetesForm
from app.test   import check

# provide login manager with load_user callback
@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Logout user
@app.route('/logout.html')
def logout():
    logout_user()
    return redirect(url_for('index'))


# Register a new user
@app.route('/register.html', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    msg = None

    if request.method == 'GET': 
        return render_template('layouts/auth-default.html',
                                content=render_template( 'pages/register.html',
                                form=form, msg=msg ) )

    # check if both http method is POST and form is valid on submit
    if form.validate_on_submit():
        password        = request.form.get('password', '', type=str) 
        email           = request.form.get('email'   , '', type=str).lower()
        confirmPassword = request.form.get('confirm_password', '', type=str)
        user_by_email   = User.query.filter_by(email=email).first()
        
        if confirmPassword == password:
            if user_by_email:
                msg = 'Error: User exists!'
            else:         
                pw_hash = password #bc.generate_password_hash(password)
                user = User(email, pw_hash)
                user.save()
                msg = 'User created, please <a href="' + url_for('login') + '">login</a>'
        else:
            msg = "Error: Password do not match."     
    else:
        msg = 'Input error'     

    return render_template('layouts/auth-default.html',
                            content=render_template( 'pages/register.html',
                            form=form, msg=msg ) )



# Authenticate user
@app.route('/login.html', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    msg = None
    if form.validate_on_submit():
        email    = request.form.get('email', '', type=str).lower()
        password = request.form.get('password', '', type=str) 
        user = User.query.filter_by(email=email).first()
        if user:
            #if bc.check_password_hash(user.password, password):
            if user.password == password:
                login_user(user)
                return redirect(url_for('index'))
            else:
                msg = "Wrong password. Please try again."
        else:
            msg = "Unknown user"

    return render_template('layouts/auth-default.html',
                            content=render_template( 'pages/login.html', form=form, msg=msg ) )


   
@app.route('/update', methods = ['GET', 'POST'])
def update():
    form = ProfileUpdateForm(request.form)
    msg = None
    error = None
    if form.validate_on_submit():
        email = request.form.get('email', '', type=str).lower()
        user = User.query.filter_by(email=email).first()        
        if user:
            user.firstname     = request.form.get('firstname',   '',  type=str)
            user.lastname      = request.form.get('lastname',    '',  type=str)
            user.address       = request.form.get('address',     '',  type=str)
            user.email         = request.form.get('email',       '',  type=str)
            user.country       = request.form.get('country',     '',  type=str)
            user.description   = request.form.get('description', '',  type=str)
            user.city          = request.form.get('city',        '',  type=str)
            user.phone         = request.form.get('phone',       '',  type=str)
            db.session.commit()
            msg = "Successfully Updated."
        else:
            error = "Error while updating."  
            
    return render_template('layouts/default.html',
                            content=render_template( 'pages/profile.html', form=form, msg=msg, error= error ) )
    


@app.route('/detect-diabetes', methods=[ "POST" ])
def detectDiabetes():
    form  = DetectDiabetesForm(request.form)
    msg   = None
    result = None
    base_dir = os.path.abspath(os.path.dirname(__file__))
    print(request.form.get('pregnancies'))
    if form.validate_on_submit():
        data = []
        data.append(request.form.get('pregnancies'))
        data.append(request.form.get('glucose'))
        data.append(request.form.get('bloodPressure'))
        data.append(request.form.get('skinThickness'))
        data.append(request.form.get('insulin'))
        data.append(request.form.get('bmi'))
        data.append(float(request.form.get('pedigreeFunction')))
        data.append(request.form.get('age'))
        result = check(base_dir, data)   
    return render_template('layouts/default.html',
                                content=render_template( 'pages/detect-diabetes.html', form = form, msg= msg, result =result))
    



# App main route + generic routing
@app.route('/', defaults={'path': 'detect-diabetes.html'})
@app.route('/<path>')
def index(path):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    try:
        form = ProfileUpdateForm(request.form)
        msg= None
        error = None
        # try to match the pages defined in -> pages/<input file>
        return render_template('layouts/default.html',
                                content=render_template( 'pages/'+path, form = form, msg= msg, error =error))
    except Exception:

        return render_template('layouts/auth-default.html',
                                content=render_template( 'pages/404.html' ) )
        
