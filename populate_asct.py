__author__ = 'Alexey Kutepov'

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'asct.settings')
import django
django.setup()
from django.contrib.auth.models import User

def populate():
    """
    Populates the database.
    :return:
    """
    add_super_user()


def add_super_user():
    """
    Creates a superuser
    :return:
    """
    try:
        user = django.contrib.auth.get_user_model().objects.create_superuser(
            email="admin@gmail.com",
            date_of_birth="1990-01-01",
            password="admin"
        )
        return user
    except:
        print("Impossible to create a superuser.")


def add_user(email, password, first_name, middle_name, last_name, birthday, gender):
    """
    Creates new user into database
    :param email:
    :param password:
    :param first_name:
    :param middle_name:
    :param last_name:
    :param birthday:
    :param gender
    :return:
    """
    user_profile = django.contrib.auth.get_user_model().objects.create_user(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
        middle_name=middle_name,
        date_of_birth=birthday,
        gender=gender,
    )
    return user_profile



if __name__ == '__main__':
    print("Starting ASCT population script...")
    populate()
    print("Complete!")