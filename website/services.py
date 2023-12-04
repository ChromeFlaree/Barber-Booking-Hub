from .models import User

def get_user_info(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user:
        return {
            'name': user.first_name, 
            'email': user.email
        }
    else:
        return None