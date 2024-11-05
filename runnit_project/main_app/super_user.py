

from main_app import db

from .models import Superuser

superuser = Superuser(username='admin', email='admin@example.com', 
                 password='admin001')




db.session.add(superuser)
db.session.commit()