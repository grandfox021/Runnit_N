from . import db
from werkzeug.security import generate_password_hash,check_password_hash   # type: ignore
from datetime import datetime
from sqlalchemy import Enum as SQLAEnum
from enum import Enum

class ResumeStatus(Enum):
    P = "Pending"
    A = "Approved"
    D = "Declined"
# Resume Model


# User table with one-to-many relationship with Post and Comment
# User Model
class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone_number = db.Column(db.String(15), nullable=True)
    profile_pic = db.Column(db.String(200))
    resume = db.Column(db.String(150), nullable=True)  # Stores the resume file path
    resume_approved = db.Column(SQLAEnum(ResumeStatus), nullable=True)
    iqtest_score = db.Column(db.Integer, nullable=True)
    _password = db.Column(db.String(250), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_superuser = db.Column(db.Boolean, default=False)
    is_authenticated = db.Column(db.Boolean, default=False)


    # Relationships
    posts = db.relationship('Post', backref='user', lazy=True)
    comments = db.relationship('Comment', backref='user', lazy=True)
    ratings = db.relationship('Rating', backref='user', lazy=True)
    resume = db.relationship("Resume", back_populates="user", uselist=False)  # uselist=False ensures one-to-one
    course = db.relationship('Course', backref='user', lazy=True)
    iqtest = db.relationship('IQTest', backref='user', lazy=True)
    # Discriminator column (to distinguish child classes)
    type = db.Column(db.String(50))



    def set_auth_true(self) :
        self.is_authenticated = True

    def set_auth_false(self) :
        self.is_authenticated = False

    def __repr__(self):
        return f'<User {self.email}>'

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        self._password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)

    def verify_password(self, password):
        return check_password_hash(self._password, password)

    def verify_phone_number(self):
        pass

    def verify_email(self):
        pass

# Superuser inherits User
class Superuser(User):

    def __init__(self, firstname, lastname, email, password, **kwargs):
        # Call the parent class (User) __init__ method to set base attributes
        super().__init__(firstname=firstname, lastname=lastname, email=email, password=password, **kwargs)
        self.is_superuser = True

    def promote_user_to_admin(self, user):
        user.is_admin = True
        db.session.commit()

# Admin inherits User
class Admin(User):

    def __init__(self, firstname, lastname, email, password, **kwargs):
        # Call the parent class (User) __init__ method to set base attributes
        super().__init__(firstname=firstname, lastname=lastname, email=email, password=password, **kwargs)
        self.is_admin = True

    def create_post(self, post):
        db.session.add(post)
        db.session.commit()

    def update_post(self, post, new_data):
        post.title = new_data['title']
        post.body = new_data['body']
        db.session.commit()

    def delete_post(self, post):
        db.session.delete(post)
        db.session.commit()

    def submit_grade(self, grade):
        db.session.add(grade)
        db.session.commit()

    def submit_course(self, course):
        db.session.add(course)
        db.session.commit()

    def calculate_average_rating_submitted(self):
        pass


class Participant(db.Model):
    __tablename__ = 'participants'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.course_id'), nullable=False)
    date_joined = db.Column(db.DateTime, default=datetime.now())

    # Relationships to access participant information
    user = db.relationship("User", backref="enrollments")
    course = db.relationship("Course", backref="participants")
# Post Model
class Post(db.Model):
    post_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    body = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(200),nullable = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)

# Like/Dislike Model
class LikeDislike(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.post_id'), nullable=False)
    like = db.Column(db.Boolean, default=True)

# Comment Model
class Comment(db.Model):
    comment_id = db.Column(db.Integer, primary_key=True)
    commenter_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    body = db.Column(db.Text(500), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.post_id'), nullable=False)

    def __repr__(self):
        return f'<Comment {self.body[:20]}>'

# Intern inherits User
class Intern(User):
    def __init__(self, firstname, lastname, email, password, **kwargs):
        # Call the parent class (User) __init__ method to set base attributes
        super().__init__(firstname=firstname, lastname=lastname, email=email, password=password, **kwargs)

    MBTI_test_grade = db.Column(db.String(100))
    IQ_test_grade = db.Column(db.Integer)
    course_exam_grade = db.Column(db.String(100))
    average_grade = db.Column(db.Float)

    def submit_resume(self, resume):
        db.session.add(resume)
        db.session.commit()

    def submit_mbti_test(self, mbti_test):
        db.session.add(mbti_test)
        db.session.commit()

    def submit_iq_test(self, iq_test):
        db.session.add(iq_test)
        db.session.commit()



class Resume(db.Model):
    resume_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    file_path = db.Column(db.String(150), nullable=False)  # Path to the resume file
    approved = db.Column(SQLAEnum(ResumeStatus), nullable=True)   
    description = db.Column(db.Text, nullable=True)
    profile_image = db.Column(db.String(200))
    skill = db.Column(db.String(200))
    user = db.relationship("User", back_populates="resume")
    def verify_format_pdf(self):
        pass

# IQ Test Model
class IQTest(db.Model):
    test_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    test_result = db.Column(db.Integer)

# MBTI Test Model
class MBTITest(db.Model):
    test_id = db.Column(db.Integer, primary_key=True)
    intern_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    test_result = db.Column(db.String(100))

# Course Model
class Course(db.Model):
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    course_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    body = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer)
    image = db.Column(db.String(200))
    closed = db.Column(db.Boolean, default=False)
    # Defined a property to count participants
    @property
    def participant_count(self):
        return len(self.participants)
    
    def change_coursename(self, new_name):
        self.name = new_name
        db.session.commit()

    def calculate_average_ratings_submitted(self):
        pass


# Exam Model
class Exam(db.Model):
    exam_id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.course_id'), nullable=False)
    exam_name = db.Column(db.String(100), nullable=False)

# Grade Model
class Grade(db.Model):
    grade_id = db.Column(db.Integer, primary_key=True)
    exam_id = db.Column(db.Integer, db.ForeignKey('exam.exam_id'), nullable=False)
    intern_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    grade = db.Column(db.String(10), nullable=False)

# Rating Model
class Rating(db.Model):
    rate_id = db.Column(db.Integer, primary_key=True)
    intern_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.course_id'), nullable=False)

    def submit_rating_to_admin(self):
        pass

    def submit_rating_to_course(self):
        pass


