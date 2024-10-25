from main_app import app,db
from main_app.models import Superuser,Admin
from flask import session



def create_superuser(firstname, lastname, email, password):
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
            password=password
        )

        db.session.add(superuser)
        db.session.commit()
        print('Superuser created successfully!')



def create_admin(firstname, lastname, email, password):
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
            password=password
        )

        db.session.add(admin)
        db.session.commit()
        print('Admin created successfully!')


# Create a flag to ensure initialization happens only once
initialization_done = False


@app.before_request
def create_initials():
    global initialization_done
    if not initialization_done:
        db.create_all()
        
        create_admin(
        firstname="hassan",
        lastname="bouzarpour",
        email="hbtk320@gmail.com",
        password="ha001"
        )


        create_admin(
        firstname="melika",
        lastname="ebrahimi",
        email="melika@example.com",
        password="me001"
        )



        if not "language" in session:
            session["language"] = 'fa'

        initialization_done = True




if __name__ == '__main__' :
       
    app.run(debug=True)   