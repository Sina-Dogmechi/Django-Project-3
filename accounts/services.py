from .models import User


def create_user(*, email, username, password):
    user = User(email=email, username=username)
    user.set_password(password)
    user.save()
    return user


def update_profile(*, user, username):
    user.username = username
    user.save(update_fields=['username'])
    return user


def change_password(*, user, new_password):
    user.set_password(new_password)
    user.save(update_fields=['password'])
    return user


def deactivate_user(*, user):
    user.is_active = False
    user.save(update_fields=['is_active'])
    return user