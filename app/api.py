import os
from app.models import User
from app        import app, db, bc
from flask      import request, make_response, jsonify, render_template
from app.test   import checkUsingKNN, checkUsingNaiveBayes, checkUsingDT


PREFIX = "/api"
@app.route(PREFIX+'/login', methods=[ "POST" ])
def api_login():
    email = request.form.get('email').strip()
    password = request.form.get('password').strip()
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
            return jsonify(data), 200
        else:
            msg = "Incorrect password. Please try again." 
    else:
        msg = "Incorrect email or password."
    return jsonify({"error":msg}), 422



@app.route(PREFIX+"/register", methods=[ "POST" ])
def api_register():
    password        = request.form.get('password',         '', type=str) 
    email           = request.form.get('email'   ,         '', type=str).lower()
    confirmPassword = request.form.get('confirm_password', '', type=str)
    user_by_email   = User.query.filter_by(email=email).first()
    
    if confirmPassword == password:
        if user_by_email:
            msg = 'User exists already.'
        else:         
            pw_hash = bc.generate_password_hash(password)
            user = User(email, pw_hash)
            user.save()
            return jsonify({'success': 'User created successfully'}), 200
    else:
        msg = 'Password do not match'
    
    return jsonify({'error':msg}), 422
    


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

  
          
@app.errorhandler(Exception)
def unhandled_exception(e):
    return render_template('layouts/auth-default.html',
                                content=render_template( 'pages/404.html' ) )