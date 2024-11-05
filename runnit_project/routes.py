from flask import session,request,flash,redirect,render_template,url_for,jsonify # type: ignore
from .translations import translations
from flask_mailman import Mail,EmailMessage  # type: ignore
from .decorators import admin_required,login_required
import os
from .forms import PostForm,CourseForm,PhoneNumberForm,VerificationForm,ResumeUploadForm
from itsdangerous import URLSafeTimedSerializer
from . import app,db,TWILIO_ACCOUNT_SID,TWILIO_AUTH_TOKEN,TWILIO_PHONE_NUMBER
from . import DEFAULT_IMAGE_PATH_FOR_COURSE,DEFAULT_IMAGE_PATH_FOR_POST,DEFAULT_IMAGE_PATH_FOR_USER,DEFAULT_PATH_FOR_RESUME
from .models import User,Post,Superuser,Admin,Course,Resume,Comment,Participant,IQTest
from werkzeug.utils import secure_filename
from twilio.rest import Client
import random

s = URLSafeTimedSerializer(app.secret_key)
mail = Mail(app)

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


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
    sliders = [{'title': 'test', 'image': 'test.jpg'},{'title': 'test2', 'image': 'test2.png'}]
    if "user_id" in session :
        user_id = session.get("user_id")
        user = User.query.filter_by(user_id = user_id).first()

        
    else :
        user = None

    show_header = True
    return render_template("home.html", user = user, sliders = sliders, show_header=show_header )

@app.route("/admin")
def admin() :
    return render_template("admin/index.html")


@app.route("/courses", methods=['GET'])
def courses() :

    courses = Course.query.all()
    show_header = True

    return render_template("course_list.html", courses=courses, show_header=show_header)




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
                session.permanent = True  # Use permanent sessions to apply lifetime
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
        image =  DEFAULT_IMAGE_PATH_FOR_USER 
        if User.query.filter_by(email=email).first() :
            flash(translations[session['language']]['username_already_taken'],"info") 
            return redirect(url_for("signup"))

        # hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
        new_user = User(firstname=first_name,lastname = last_name ,email = email, password=password,profile_pic = image)
        
        db.session.add(new_user)
        db.session.commit()
        
        session.permanent = True  # Use permanent sessions to apply lifetime
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


def send_course_declined_email(to_email):

    title = "وضعیت درخواست شما برای شرکت در در دوره"
    body = F"hello this is a message from support to reset your pass please follow the link :"
    sender_email = "hbsmtp635@gmail.com"
    reciever_email = [to_email]
    msg = EmailMessage(subject=title,body=body,from_email=sender_email,to=reciever_email)
    msg.send()
    return "message sent successfully check your inbox"

    

def send_course_approved_email(to_email):


    title = "وضعیت درخواست شما برای شرکت در در دوره"
    body = F"hello this is a message from support to reset your pass please follow the link :"
    sender_email = "hbsmtp635@gmail.com"
    reciever_email = [to_email]
    msg = EmailMessage(subject=title,body=body,from_email=sender_email,to=reciever_email)
    msg.send()
    return "message sent successfully check your inbox"


def send_course_waiting_email(to_email):
    

    title = "وضعیت درخواست شما برای شرکت در در دوره"
    body = F"hello this is a message from support to reset your pass please follow the link :"
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



@app.route("/create_post", methods=["GET", "POST"])
@admin_required
@login_required
def create_post():
    form = PostForm()
    
    if form.validate_on_submit():  # This checks if the form is submitted and valid
        title = form.title.data
        body = form.body.data
        image = form.image.data  # Handle the file upload if provided
        if image and image.filename !="":
            if allowed_file(image.filename):  # Check if an image was uploaded
                filename = secure_filename(image.filename)
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image.save(image_path)
            else:
                flash(translations[session['language']]['not_supported_format']) 
                return redirect(url_for('create_post'))
        else:
            image_path = DEFAULT_IMAGE_PATH_FOR_POST  # Use default image if no image was uploaded

 
        user_id = session['user_id']  

        # Save the new post to the database
        post = Post(title=title, body=body, image=image_path, user_id=user_id)

        db.session.add(post)
        db.session.commit()

        flash('Post created successfully!', 'success')
        return redirect(url_for('home'))

    return render_template('create_post.html', form=form)


@app.route("/admin-panel")
@admin_required    
@login_required
def admin_panel():

    user_id = session["user_id"]

    user = User.query.filter_by(user_id = user_id).first()
    courses = Course.query.filter_by(user_id = user_id)
    posts = Post.query.filter_by(user_id = user_id)

    
    return render_template("admin_panel.html",user=user,courses = courses,posts=posts)



@login_required
@app.route('/enter_phone', methods=['GET', 'POST'])
def enter_phone():
    form = PhoneNumberForm()
    if form.validate_on_submit():
        phone_number = form.phone.data
        verification_code = str(random.randint(100000, 999999))  # Generate 6-digit code
        session['verification_code'] = verification_code
        session['phone_number'] = phone_number

        # Send SMS
        message = client.messages.create(
            body=f"Your verification code is {verification_code}",
            from_=TWILIO_PHONE_NUMBER,
            to=phone_number
        )
        flash(f'Code sent to {phone_number}', 'info')
        return redirect(url_for('verify_phone'))
    return render_template('enter_phone.html', form=form)


@app.route('/verify_phone', methods=['GET', 'POST'])
def verify_phone():
    form = VerificationForm()
    if form.validate_on_submit():
        entered_code = form.verification_code.data
        if entered_code == session.get('verification_code'):
            flash('Phone number verified successfully!', 'success')
            user = User.query.filter_by(user_id = session.get('user_id'))
            phone_number = session.get('phone_number')
            user.phone_number = phone_number
            db.session.commit()
            return redirect(url_for('success'))
        else:
            flash('Incorrect verification code. Please try again.', 'danger')
    return render_template('verify_phone.html', form=form)

@app.route('/success')
def success():
    return "Phone number verified successfully!"



@app.route("/create_course", methods=["GET", "POST"])
@login_required
def create_course():
    form = CourseForm()
    if form.validate_on_submit():
        user_id = session.get("user_id")
        name = form.name.data
        body = form.body.data
        image = request.files['image']

        # Debugging statements to identify the type of 'image'
        print("Image data type:", type(image))
        print("Image data:", image)

        # Check if 'image' is an actual file
        if image and image.filename != '':
            if allowed_file(image.filename):  # Check if image has an allowed format
                filename = secure_filename(image.filename)
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image.save(image_path)
            else:
                flash(translations[session['language']]['not_supported_format'])
                return redirect(url_for('create_course'))
        else:
            image_path = DEFAULT_IMAGE_PATH_FOR_COURSE  # Use default image if no image was uploaded

        # Create a new Course instance with data from the form
        new_course = Course(
            user_id=user_id,
            name=name,
            body=body,
            image=image_path
        )
        
        # Add and commit the new course to the database
        db.session.add(new_course)
        db.session.commit()
        
        flash("Course created successfully!", "success")
        return redirect(url_for("courses"))
    
    return render_template("create_course.html", form=form)

@app.route("/about-us")
def about_us():

    return render_template("about.html")


@app.route("/post/<int:post_id>",methods = ["POST","GET"])
def post_detail(post_id):
    post = Post.query.filter_by(post_id=post_id).first()

    if "user_id" in session:
        user= User.query.get_or_404(session['user_id'])
        user_id = session.get("user_id")

    else:
        user=""

    if request.method == "POST" and "comment_submit" in request.form:

        comment = request.form['comment']
        new_comment = Comment(body = comment , post_id = post_id , commenter_id =user_id )
        db.session.add(new_comment)
        db.session.commit()
        return redirect(url_for('post_detail',post_id = post_id))


    comments = Comment.query.filter_by(post_id=post_id).all()
    return render_template("post_detail.html" , post=post,comments = comments, translations=translations[session["language"]])

@login_required
@app.route('/user/account')
def user_account():

    user_id= session['user_id']
    user = User.query.filter_by(user_id = user_id).first()
    
    return render_template("account.html",user = user)

@app.route("/detail_demo")
def detail_post_demo() :

    return render_template("single.html")

@app.route("/all-posts")
def all_posts():

    posts = Post.query.all()
    show_header = True

    return render_template("all_posts.html", posts = posts,translations=translations[session["language"]], lang=session["language"], show_header=show_header)


@app.route("/recent_users_comments")
def recent_users_comments():

    return render_template("comment.html")



@app.route("/course-detail/<int:course_id>")
def course_detail(course_id):

    course = Course.query.filter_by(course_id = course_id).first()
    return render_template("course_detail.html",course = course)




@app.route("/enroll_course/<int:course_id>", methods=["POST","GET"])
@login_required
def enroll_course(course_id):
    # Check if the course exists
    course = Course.query.get_or_404(course_id)
    user_id = session.get("user_id")
    user = User.query.get(user_id)  

    if not user.resume:
        flash( "ابتدا رزموه خود را در پروفایل آپلود کنید سپس درخواست دهید")
        return redirect(url_for("upload_resume"))
    elif not user.resume.approved:
        flash("رزومه شما در حال بررسی است  در صورت تایید به شما از طریق ایمیل اطلاع رسانی میشود")
        return redirect(url_for("course_detail",course_id=course_id))

    if not user.iqtest_score:
        flash("ابتدا در آزمون شرکت کنید تا نمره شما محاسبه شود  سپس درخواست دهید")
        return redirect(url_for('user_account'))
    
    # # If resume is approved, proceed with enrollment
    # course.users.append(user)  # Assuming a relationship between users and courses
    # db.session.commit()
    # flash("You have successfully enrolled in the course!")
    # return redirect(url_for("course_detail", course_id=course.id))

    resume = Resume.query.filter_by(user_id = user_id).first()
    if resume.course_id is not None:
        flash("رزومه شما درحال بررسی است درصوت تایید به شما از طریق ایمیل یا تماس تلفنی اطلاع داده میشود")
        return redirect(url_for("course_detail",course_id=course_id)) 
    elif resume.course_id is None:
        resume.course_id = course_id
        db.session.commit()
        flash("شما با موفقیت درخواست خود را ثبت کرده اید , یعد از بررسی رزومه نتیجه به شما اطلاع داده میشود", "success")
        return redirect(url_for("course_detail", course_id=course_id))

    if user.resume_approved == "D" :
        flash("متاسفانه رزومه شما پیرفته نشده است. به امید همکاری در فرصت های آینده")
        return redirect(url_for("course_detail",course_id=course_id))
    # Check if the user is already enrolled
    existing_participant = Participant.query.filter_by(user_id=session.get("user_id"), course_id=course_id).first()
    if existing_participant:
        flash("You are already enrolled in this course.", "info")
        return redirect(url_for("course_detail", course_id=course_id))



    flash("شما با موفقیت درخواست خود را ثبت کرده اید , یعد از بررسی رزومه نتیجه به شما اطلاع داده میشود", "success")
    return redirect(url_for("course_detail", course_id=course_id))


@app.route("/upload_resume", methods=["GET", "POST"])
@login_required
def upload_resume():
    user = User.query.filter_by(user_id = session.get("user_id"))
    form = ResumeUploadForm()
    if form.validate_on_submit():
        resume_file = form.resume.data
        filename = secure_filename(resume_file.filename)
        if filename == '':
            flash("no file selected")
            return redirect(url_for('upload_resume'))
        filename = secure_filename(resume_file.filename)
        resume_path = os.path.join(DEFAULT_PATH_FOR_RESUME, filename)  # Specify your upload folder path
        resume_file.save(resume_path)

        # Check if a resume already exists and update it, or create a new one
        existing_resume = Resume.query.filter_by(user_id=session.get("user_id")).first()
        if existing_resume :
            if existing_resume.approved == "A" :
                flash("رزومه شما قبلا مورد تایید قرار گرفته و نیازی  به آپلود رزمه جدید ندارید")
                return redirect(url_for('user_account'))

            existing_resume.file_path = filename
            existing_resume.approved = "P"  # Reset approval status on new upload
        else:
            user.resume = resume_path
            new_resume = Resume(file_path=filename, approved="P", user_id=session.get("user_id"))
            db.session.add(new_resume)

        db.session.commit()
        flash("رزومه شما با موفقیت آپلود شد")
        return redirect(url_for("user_account"))
    return render_template("upload_resume.html", form=form)

@app.route("/close-course/<int:course_id>")
@admin_required
@login_required
def close_course(course_id):

    course = Course.query.filter_by(course_id = course_id)
    course.closed  = True
    db.session.commit()
    flash("دوره با موفقیت بسته شد")
    return redirect(url_for('admin_panel'))

@app.route("/open-course/<int:course_id>")
@admin_required
@login_required
def open_course(course_id):

    course = Course.query.filter_by(course_id = course_id)
    course.closed  = False
    db.session.commit()
    flash("دوره با موفقیت باز شد")
    return redirect(url_for('admin_panel'))


@app.route('/course/<int:course_id>/resumes',methods=["POST","GET"])
def view_course_resumes(course_id):
    # Get the course and associated resumes

    course = Course.query.get_or_404(course_id)
    resumes = Resume.query.filter_by(course_id=course_id,approved="P").all()  # Assuming course_id exists in Resume

    return render_template('view_course_resumes.html', course=course, resumes=resumes)

# @app.route("/admin/review_resumes")
# def review_resumes():
#     pending_resumes = Resume.query.filter_by(approved=False).all()
#     return render_template("admin/review_resumes.html", pending_resumes=pending_resumes)


@app.route("/admin/approve_resume/<int:resume_id>/<int:course_id>", methods=["POST","GET"])
def approve_resume(resume_id,course_id):
    resume = Resume.query.get_or_404(resume_id)
    user = User.query.filter_by( user_id = resume.user_id).first()
    user.resume_approved = "A"
    resume.approved = "A"
    participant = Participant(user_id=session.get("user_id"), course_id=course_id)
    db.session.add(participant)
    db.session.commit()
    db.session.commit()
    send_course_approved_email(user.email)
    flash("Resume approved successfully.")
    return redirect(url_for("review_resumes"))

@app.route("/admin/reject_resume/<int:resume_id>", methods=["POST","GET"])
def reject_resume(resume_id):
    resume = Resume.query.get_or_404(resume_id)
    user = User.query.filter_by( user_id = resume.user_id).first()
    send_course_declined_email(user.email)
    user.resume_approved = "D"
    resume.approved = "D"
    # db.session.delete(resume)  # Remove the resume if rejected
    db.session.commit()
    flash("Resume rejected.")
    return redirect(url_for("review_resumes"))


@app.route('/submit_iq_test', methods=['POST','GET'])
@login_required
def submit_iq_test():
    user = User.query.filter_by(user_id =session.get("user_id")).first()
    if request.method == "POST" :
        # Define the correct answers for each question
        correct_answers = {
            "q1": "30",
            "q2": "یکشنبه",
            "q3": "0",
            "q4": "54",
            "q5": "9",
            "q6": "آلمان",
            "q7": "22.5",
            "q8": "7",
            "q9": "10",
            "q10": "5",
            "q11": "75",
            "q12": "15",
            "q13": "8",
            "q14": "2",
            "q15": "4",
            "q16": "4",
            "q17": "360",
            "q18": "52",
            "q19": "49",
            "q20": "8"
        }
        # Retrieve user responses
        user_answers = request.form.to_dict()
        
        # Calculate the score
        score = 0
        for question, correct_answer in correct_answers.items():
            if question in user_answers and user_answers[question].strip() == correct_answer:
                score += 1
        iqtest = IQTest(user_id = user.user_id , test_result = score)
        user.iqtest_score = score
        db.session.add(iqtest)
        db.session.commit()
        flash("نمره شما در آزمون ثبت شد")
        # Redirect to home with score (adjust as necessary for your home view)
        return redirect(url_for('user_account'))
    else :
        return render_template("IQtest.html")


@app.route("/course-participants/<int:course_id>")
@admin_required
@login_required
def view_course_participants(course_id):


    participants =Participant.query.filter_by(course_id = course_id)


    return render_template("course_participants.html",participants = participants)



@app.route("/course-participants/<int:participant_id>", methods=['POST','GET'])
@admin_required
@login_required
def delet_participants(participant_id):



    participant  = Participant.query.filter_by(id =participant_id ).first()
    course_id = participant.course_id
    db.session.delete(participant)
    db.session.commit()

    flash("شرکت کننده از دوره حذف شد")
    return redirect(url_for('view_course_participants',course_id = course_id))
