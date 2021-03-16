# Python modules
import os, logging 

# Flask modules
from flask               import render_template, request, url_for, redirect, send_from_directory, flash
from flask_login         import login_user, logout_user, current_user, login_required
from werkzeug.exceptions import HTTPException, NotFound, abort
from app                 import api
from flask_mail          import Message

# App modules
from app        import app, lm, db, bc, mail
from app.models import User
from app.forms  import LoginForm, RegisterForm, ProfileUpdateForm, DetectDiabetesForm, PasswordResetForm
from app.test   import checkUsingKNN, checkUsingNaiveBayes, checkUsingDT

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
        password        = request.form.get('password',         '', type=str) 
        email           = request.form.get('email'   ,         '', type=str).lower()
        confirmPassword = request.form.get('confirm_password', '', type=str)
        user_by_email   = User.query.filter_by(email=email).first()
        
        if confirmPassword == password:
            if user_by_email:
                msg = 'Error: User exists!'
            else:         
                pw_hash = bc.generate_password_hash(password)
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
            if bc.check_password_hash(user.password, password):
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
    navieBayesResult = None
    knnResult = None
    base_dir = os.path.abspath(os.path.dirname(__file__))
    if form.validate_on_submit():
        data = []
        data.append(int(request.form.get('pregnancies')))
        data.append(int(request.form.get('glucose')))
        data.append(int(request.form.get('bloodPressure')))
        data.append(int(request.form.get('skinThickness')))
        data.append(int(request.form.get('insulin')))
        data.append(float(request.form.get('bmi')))
        data.append(float(request.form.get('pedigreeFunction')))
        data.append(int(request.form.get('age')))
        knnResult = checkUsingKNN(base_dir, data)        
        navieBayesResult = checkUsingNaiveBayes(base_dir, data)
        decisionTreeResult = checkUsingDT(base_dir, data)
        
    return redirect(url_for('detectDiabetesPage', msg=msg, 
                            knnResult=knnResult, 
                            navieBayesResult=navieBayesResult, dtResult= decisionTreeResult ))



@app.route('/detect-diabetes.html', methods=["GET", "POST"])
def detectDiabetesPage():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    msg = request.args.get('msg')
    knnResult = request.args.get('knnResult')
    navieBayesResult = request.args.get('navieBayesResult')
    decisionTreeResult = request.args.get('decisionTreeResult')
    form  = ProfileUpdateForm(request.form) 
    
    return render_template('layouts/default.html', 
                           content = render_template('pages/detect-diabetes.html', 
                           form=form, msg=msg, knnResult=knnResult, 
                           navieBayesResult=navieBayesResult,
                           decisionTreeResult=decisionTreeResult))
    

@app.route('/send_email', methods=[ "GET" ])
def send_email():
    email = request.args.get('email')
    user = User.query.filter_by(email=email).first()
    if user:
        try :
            send_email_to_user(user)
            response = {
                'data':"Password reset link has been sent to your email.",
                'status_code': '200'
            }
        except Exception as e:
            print(e)
            response = {
                'data':"Could not send email at this moment.",
                'status_code': '500'
            }
    else:
        response = {
            'data':"Email does not exist.",
            'status_code': '400'
        }
    return response

@app.route("/reset_password_request/<token>", methods=[ 'GET', 'POST' ])
def password_reset_view(token):
    token =token
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is inavlid or expired token', 'warning')
        return redirect(url_for('login'))
    form = PasswordResetForm()
    return render_template('layouts/auth-default.html',
                            content=render_template( 'pages/reset_password.html', title='Reset Password', form = form, token=token))
        
        
def send_email_to_user(user):
    token = User.get_reset_token(user)
    msg = Message('Password Reset Request',
                   sender='noreply@demo.com', 
                   recipients = [user.email])
    msg.body = '''To reset your password visit the following link:
'''+url_for('password_reset_view', token=token, _external=True)+'''

If you did not make this request than ignore this mail.
'''
    mail.send(msg)
   
    
@app.route("/reset-password", methods=[ "GET", "POST"])
def reset_password():
    msg = None
    if current_user.is_authenticated:
        return redirect(url_for('/'))
    form = PasswordResetForm()
    loginForm = LoginForm()
    if form.validate_on_submit():
        user = User.verify_reset_token(request.form.get('token'))
        if user:
            password = request.form.get('password')
            user.password = bc.generate_password_hash(password)
            db.session.commit()
            msg = "Password changed. Now you can login."
        else:
            msg = "Sorry Invalid token."
    return render_template('layouts/auth-default.html',
                        content=render_template( 'pages/login.html', form=loginForm, msg=msg ) )

# App main route + generic routing
@app.route('/', defaults={'path': 'detect-diabetes.html'}, methods=["GET", "POST"])
@app.route('/<path>')
def index(path):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    
    try:
        form = ProfileUpdateForm(request.form)
        msg = None
        error = None
        return render_template('layouts/default.html',
                                content=render_template( 'pages/'+path, form = form,
                                                         msg= msg, error =error))
    except Exception:
        return render_template('layouts/auth-default.html',
                                content=render_template( 'pages/404.html' ) )
        
