import os
from app.models import User
from app        import app, db, bc, mail
from flask_mail import Message
from flask      import request, make_response, jsonify, render_template, url_for
from app.test   import checkUsingKNN, checkUsingNaiveBayes, checkUsingDT


PREFIX = "/api"
@app.route(PREFIX+'/login', methods=[ 'GET', 'OPTIONS', 'POST'])
def api_login():
    dat = {
        'Allow' : ['POST', 'OPTIONS'],
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': ['DELETE', 'GET', 'HEAD', 'OPTIONS', 'PATCH', 'POST', 'PUT']
    }
    if request.method == 'OPTIONS':
        return jsonify({}), 200, dat
    print(str(request.args) + 'sdlfjkdsljf')
    email = request.json['email'].strip()
    password = request.json['password'].strip()
    user = User.query.filter_by(email=email).first()
    if user:
        if bc.check_password_hash(user.password, password):
            data = {
                "id"    : user.id,
                "name"  : (user.firstname +" " + User.lastname) if (user.firstname and user.lastname) else "",
                "email" : user.email,
                "phone" : user.phone if (user.phone) else "",
                "address" : user.address if (user.address) else ""
            }
            return jsonify(data), 200, dat
        else:
            msg = "Incorrect password. Please try again."   
    else:
        msg = "Incorrect email or password."
    return jsonify({"error":msg}), 422, dat



@app.route(PREFIX+"/register", methods=[ "GET", "POST", "OPTIONS"])
def api_register():
    # try:
    dat = {
            'Allow' : ['POST', 'OPTIONS'],
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': ['DELETE', 'GET', 'HEAD', 'OPTIONS', 'PATCH', 'POST', 'PUT']
        }
    if request.method == 'OPTIONS':
        return jsonify({}), 200, dat
    password        = request.json['password']
    email           = request.json['email'].lower()
    confirmPassword = request.json['confirm_password']
    user_by_email   = User.query.filter_by(email=email).first()
    
    if confirmPassword == password:
        if user_by_email:
            msg = 'User exists already.'    
        else:         
            pw_hash = bc.generate_password_hash(password)
            user = User(email, pw_hash)
            user.save()
            return jsonify({'success': 'User created successfully'}), 200, dat
    else:
        msg = 'Password do not match'
    
    return jsonify({'error':msg}), 422, dat
    # except (Exception):
        # return jsonify({'error':'error'}), 422, dat


@app.route(PREFIX+'/update', methods = ['POST'])
def api_update():
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
        msg = "Error while updating."  
    
    return jsonify({'success' : msg}), 200   
   
  
            
@app.route(PREFIX+'/detect-diabetes', methods=[ "POST" ])
def api_detectDiabetes():
    base_dir = os.path.abspath(os.path.dirname(__file__))
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
    
    return jsonify({
        "knnResult" : knnResult,
        'naiveBayesResult' : navieBayesResult,
        'decisionTreeResult' : decisionTreeResult
    }), 200

@app.route(PREFIX+'/forgot_password', methods=['GET', 'POST'])
def api_send_reset_token():
    email = request.form.get('email')
    user = User.query.filter_by(email=email).first()
    if user:
        try :
            send_email_to_user(user)
            response = {
                'data':"Password reset link has been sent to your email.",
                'status_code': '200'
            }
        except:
            response = {
                'data':"Could not send email at this moment.",
                'status_code': '500'
            }
    else:
        response = {
            'data':"Email does not exist.",
            'status_code': '422'
        }
    return response

def send_email_to_user(user):
    token = user.get_token()
    user.password_reset_token = token
    user.save()
    print(user.email)
    msg = Message('Password Reset Request',
                   sender='noreply@demo.com', 
                   recipients = [user.email])
    msg.body = '''To reset your password use this token:
token-key = '''+str(token)+'''

This is one time token and cannot be used again.
If you did not make this request than ignore this mail.
'''
    mail.send(msg)
    
@app.route(PREFIX+'/reset-password', methods=['GET', 'POST'])
def api_reset_password():
    token = request.form.get('token')
    user = User.query.filter_by(password_reset_token=token).first()
    if user:
        return jsonify({'data' : 'valid token'}), 200
    else:
        return jsonify({'data' : 'invalid token'}), 422
    
        
@app.route(PREFIX+'/change-password', methods=['GET', 'POST'])
def api_change_password():
    password = request.form.get('password')
    confirmPassword = request.form.get('confirm-password')
    token = request.form.get('token')
    user = User.query.filter_by(password_reset_token=token).first()
    if user:
        user.password_reset_token = ""
        if(confirmPassword == password):
            user.password = bc.generate_password_hash(password)
            user.save()
            return jsonify({'data' : 'password changed successful'}), 200
        else:
            return jsonify({'data' : 'password don not match'}), 422
    else:
        return jsonify({'data' : 'invalid token'}), 422
            
        
    
    
# @app.errorhandler(Exception)
# def unhandled_exception(e):
#     return render_template('layouts/auth-default.html',
#                                 content=render_template( 'pages/404.html' ) )
