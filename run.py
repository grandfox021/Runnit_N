from runnit_project.main_app import app,db
from runnit_project.main_app.models import Superuser,Admin

# def create_superuser(firstname, lastname, email, password):
#     with app.app_context():  # Make sure you're working within the Flask app context
#         # Check if superuser already exists
#         existing_user = Superuser.query.filter_by(email=email).first()
#         if existing_user:
#             print('A user with this email already exists!')
#             return

#         # Create the superuser
#         superuser = Superuser(
#             firstname=firstname,
#             lastname=lastname,
#             email=email,
#             password=password
#         )

#         db.session.add(superuser)
#         db.session.commit()
#         print('Superuser created successfully!')


def create_admin(firstname, lastname, email, password):
    with app.app_context():  # Make sure you're working within the Flask app context
        # Check if superuser already exists
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



# # Define superuser details here
# if __name__ == '__main__':
#     create_admin(
#         firstname="hassan",
#         lastname="bouzarpour",
#         email="hbtk320@gmail.com",
#         password="ha001"
#     )







if __name__ == '__main__' :
       
    app.run(debug=True)   