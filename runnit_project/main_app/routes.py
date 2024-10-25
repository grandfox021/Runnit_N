from flask import session,request,flash,redirect,render_template,url_for,jsonify # type: ignore
from .translations import translations
from flask_mailman import Mail,EmailMessage  # type: ignore
from .decorators import admin_required,login_required
import os
from .forms import PostForm
from itsdangerous import URLSafeTimedSerializer
from . import app,db
from .models import User,Post,Superuser,Admin,Course
from werkzeug.utils import secure_filename

s = URLSafeTimedSerializer(app.secret_key)
mail = Mail(app)



ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/set_language/<lang>')
def set_language(lang):
    session['language'] = lang
    return redirect(request.referrer or url_for('home'))

@app.route("/")
@app.route("/home")
def home() :

    if "user_id" in session :
        user_id = session.get("user_id")
        user = User.query.filter_by(user_id = user_id).first()

        
    else :
        user = None

    return render_template("home.html", user = user )


#region archive
@app.route("/archive", methods=['GET'])
def archive() :
    return render_template("archive.html") 
#endregion

#region account
@app.route("/account", methods=['GET'])
def account() :
    return render_template("account.html") 
#endregion
 
@app.route("/login/",methods = ['POST','GET'])
def login () :

    if "user" in session:
        flash(translations[session['language']]['already_logged_in']) 
        return redirect(url_for("home"))

    if request.method == "POST" and "sign_in" in request.form:

        email = request.form['email']
        password = request.form['password']

        # Query the user by username
        user = User.query.filter_by(email = email).first()

        if user:
            print(f"User found: {user.firstname}")  # Debugging
            print(f"Entered password: {password}")  # Debugging

            if user.verify_password(password):
                print("Password matched")  # Debugging
                session['user_id'] = user.user_id  # Store user_id in session
                session['user'] = user.firstname
                user.set_auth_true()
                flash(translations[session['language']]['login_successful']) 
                return redirect(url_for("home"))
            else:
                print("Password comparison failed")  # Debugging
                flash(translations[session['language']]['wrong_password']) 
        else:
            print("User not found")  # Debugging
            flash(translations[session['language']]['wrong_username']) 

    return render_template("login.html", translations=translations[session["language"]])



@app.route("/sign-up",methods = ["POST","GET"])
def signup() :
    if "user_id" in session :
        flash(translations[session['language']]['logout_before_signup']) 
        return redirect(url_for('home'))

    if request.method == 'POST' and "sign_up" in request.form :

        first_name = request.form['firstname']
        last_name = request.form['lastname']
        email = request.form['email']
        password = request.form['password']

        if User.query.filter_by(email=email).first() :
            flash(translations[session['language']]['username_already_taken'],"info") 
            return redirect(url_for("signup"))

        # hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
        new_user = User(firstname=first_name,lastname = last_name ,email = email, password=password)
        
        db.session.add(new_user)
        db.session.commit()
        
        session["user"] = new_user.firstname
        session["user_id"] = new_user.user_id


        flash(translations[session['language']]['congrats_account_created']) 
        return redirect(url_for("home"))
    else : 
        return render_template("register.html", translations=translations[session["language"]])



@app.route('/logout')
def logout():

    session.pop("user_id")
    session.pop("user")
    flash("you have been loged out !")
    return redirect(url_for('home'))



# function to send the reset password email
def send_reset_email(to_email, reset_link):


    title = "Password Reset Request"
    body = F"hello this is a message from support to reset your pass please follow the link : {reset_link}"
    sender_email = "hbsmtp635@gmail.com"
    reciever_email = [to_email]
    msg = EmailMessage(subject=title,body=body,from_email=sender_email,to=reciever_email)
    msg.send()
    return "message sent successfully check your inbox"




# Password reset request route
@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        if user:
            # Generate token for password reset
            token = s.dumps(email, salt='password-reset-salt')
            reset_url = url_for('reset_with_token', token=token, _external=True)
            send_reset_email(email, reset_url)
            flash("لینک تغییر پسورد برای شما ایمیل شد", "info")
            return redirect(url_for('home'))
        else:
            flash("Email not found!", "try again")
            return redirect( url_for("reset_password"))
    return render_template('reset_password.html', translations=translations[session["language"]])

# Token verification and new password submission route
@app.route('/reset/<token>', methods=['GET', 'POST'])
def reset_with_token(token):
    try:
        # Token expires after 1 hour (3600 seconds)
        email = s.loads(token, salt='password-reset-salt', max_age=3600)
    except Exception:
        flash("The reset link is invalid or has expired.", "danger")
        return redirect(url_for('index'))

    if request.method == 'POST':
        new_password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user:
            user.password = new_password
            db.session.commit()
            flash("پسورد شما با موفقیت تغییر کردید ", "success")
            return redirect(url_for('home'))

    return render_template('new_password.html', translations=translations[session["language"]])



# Define superuser details here

# @app.route("/create_post", methods=["POST", "GET"])
# @admin_required
# def create_post():
#     if request.method == "POST":
#         title = request.form['title']
#         body = request.form['body']
#         image = request.form.get('image', None)
        
#         # Assuming the admin is submitting the post
#         post = Post(title=title, body=body, image=image, user_id=session['user_id'])
#         db.session.add(post)
#         db.session.commit()

#         flash("Post successfully created!", "success")
#         return redirect(url_for('home'))
    
#     return render_template("create_post.html")



@admin_required
@login_required
@app.route("/create_post", methods=["GET", "POST"])
def create_post():
    form = PostForm()
    
    if form.validate_on_submit():  # This checks if the form is submitted and valid
        title = form.title.data
        body = form.body.data
        image = form.image.data  # Handle the file upload if provided
        if image and image.filename != '':
            if allowed_file(image.filename):  # Check if an image was uploaded
                filename = secure_filename(image.filename)
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image.save(image_path)
            else:
                flash(translations[session['language']]['not_supported_format']) 
                return redirect(url_for('create_post'))
        else:
            image_path = app.DEFAULT_IMAGE_PATH_FOR_POST  # Use default image if no image was uploaded

 
        user_id = session['user_id']  

        # Save the new post to the database
        post = Post(title=title, body=body, image=image.filename if image else None, user_id=user_id)

        db.session.add(post)
        db.session.commit()

        flash('Post created successfully!', 'success')
        return redirect(url_for('home'))

    return render_template('create_post.html', form=form)


# @admin_required
# @login_required

@login_required
@app.route("/signup_for_course")
def sign_up_for_course():
    pass
    
    
@app.route("/admin")
@admin_required    
@login_required
def admin_panel():

    user_id = session["user_id"]

    user = User.query.filter_by(user_id = user_id).first()
    courses = Course.query.filter_by(user_id = user_id)
    posts = Post.query.filter_by(user_id = user_id)
    
    return render_template("admin_panel.html",user=user,courses = courses,posts=posts)

@app.route("/resume_upload")
@login_required
def rseume_submit():


    return render_template("upload_resume.html")


@app.route("/corses")
def course() :

    return render_template("archive.html")

@app.route("/post/<int:post_id>")
def post_detail(post_id):
    post = Post.query.filter_by(post_id=post_id).first()

    return render_template("post_detail.html",post=post)

@login_required
@app.route('/user/account')
def user_account():

    user_id= session['user_id']
    intern = User.query.filter_by(user_id = user_id).first()
    
    return render_template("account.html",intern = intern)

@app.route("/detail_demo")
def detail_post_demo() :

    return render_template("single.html")

@app.route("/all-posts")
def all_posts():

    posts = Post.query.all()

    return render_template("all_posts.html", posts = posts)