from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField
from wtforms.validators import DataRequired
from wtforms import SubmitField
from wtforms.validators import DataRequired, Regexp
from flask_wtf.file import FileAllowed

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    body = TextAreaField('Body', validators=[DataRequired()])
    image = FileField('Image')


class CourseForm(FlaskForm):

    name = StringField('Title', validators=[DataRequired()])
    body = TextAreaField('Body', validators=[DataRequired()])
    image = FileField('Image')

class ResumeUploadForm(FlaskForm):
    resume = FileField("Upload Resume", validators=[FileAllowed(['pdf', 'doc', 'docx'], "Only document files are allowed!")])
    submit = SubmitField("Upload")

class PhoneNumberForm(FlaskForm):
    phone = StringField('Phone Number', validators=[
        DataRequired(),
        Regexp(r'^\+?\d{10,15}$', message="Enter a valid phone number")
    ])
    submit = SubmitField('Send Code')


class VerificationForm(FlaskForm):
    verification_code = StringField('Verification Code', validators=[DataRequired()])
    submit = SubmitField('Verify')


