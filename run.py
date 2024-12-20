from runnit_project import app,db
from runnit_project.models import Superuser,Admin
from flask import session
from runnit_project import DEFAULT_IMAGE_PATH_FOR_USER


def create_superuser(firstname, lastname, email, password,profile_pic):
    with app.app_context():  # Make sure you're working within the Flask app context
        # Check if superuser already exists
        existing_user = Superuser.query.filter_by(email=email).first()
        if existing_user:
            print('A user with this email already exists!')
            return

        # Create the superuser
        superuser = Superuser(
            firstname=firstname,
            lastname=lastname,
            email=email,
            password=password,
            profile_pic = profile_pic
        )

        db.session.add(superuser)
        db.session.commit()
        print('Superuser created successfully!')



def create_admin(firstname, lastname, email, password,profile_pic):
    with app.app_context():  # Make sure you're working within the Flask app context
        # Check if Admin already exists
        existing_user = Admin.query.filter_by(email=email).first()
        if existing_user:
            print('A user with this email already exists!')
            return

        # Create the superuser
        admin = Admin(
            firstname=firstname,
            lastname=lastname,
            email=email,
            password=password,
            profile_pic = profile_pic
        )

        db.session.add(admin)
        db.session.commit()
        print('Admin created successfully!')


# Create a flag to ensure initialization happens only once
initialization_done = False


@app.before_request
def create_initials():
    
    if not "language" in session:
        session["language"] = 'fa'

    global initialization_done
    if not initialization_done:
        db.create_all()
        
        create_admin(
        firstname="hassan",
        lastname="bouzarpour",
        email="hbtk320@gmail.com",
        password="ha001",
        profile_pic = DEFAULT_IMAGE_PATH_FOR_USER
        )


        create_admin(
        firstname="melika",
        lastname="ebrahimi",
        email="melika@example.com",
        password="me001",
        profile_pic = DEFAULT_IMAGE_PATH_FOR_USER
        )

        initialization_done = True



if __name__ == '__main__' :
       
    app.run(debug=True)   