__author__ = 'Alexey Kutepov'

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'asct.settings')

import django
django.setup()

from django.contrib.auth.models import User
from main.models import UserProfile, Company, Department

def populate():
    """
    Populates the database.
    :return:
    """
    company1 = add_company("Компания А")
    department1 = add_department(company1, "Подразделение А")
    department2 = add_department(company1, "Подразделение Б")
    company2 = add_company("Компания Б")
    department3 = add_department(company2, "Подразделение В")
    department4 = add_department(company2, "Подразделение Г")
    company3 = add_company("Компания В")
    department5 = add_department(company3, "Подразделение Д")
    department6 = add_department(company3, "Подразделение Е")

    add_super_user(company1, department1)
    add_user(
        "curator1@mail.ru",
        "123456",
        "Николаев",
        "Пётр",
        "Иванович",
        "1990-02-02",
        UserProfile.MALE,
        UserProfile.CURATOR,
        company1,
        department1,
        "Менеджер"
    )
    add_user(
        "curator2@mail.ru",
        "123456",
        "Петров",
        "Никита",
        "Сергеевич",
        "1990-03-03",
        UserProfile.MALE,
        UserProfile.CURATOR,
        company2,
        department3,
        "Менеджер"
    )
    add_user(
        "curator3@mail.ru",
        "123456",
        "Сидоров",
        "Виктор",
        "Павлович",
        "1990-04-04",
        UserProfile.MALE,
        UserProfile.CURATOR,
        company3,
        department5,
        "Менеджер"
    )
    add_user(
        "user1@mail.ru",
        "123456",
        "Иванов",
        "Иван",
        "Иванович",
        "1990-02-02",
        UserProfile.MALE,
        UserProfile.ADMIN,
        company1,
        department2,
        "Менеджер"
    )
    add_user(
        "user2@mail.ru",
        "123456",
        "Петров",
        "Пётр",
        "Петрович",
        "1990-03-03",
        UserProfile.MALE,
        UserProfile.ADMIN,
        company2,
        department4,
        "Менеджер"
    )
    add_user(
        "user3@mail.ru",
        "123456",
        "Сидоров",
        "Сидор",
        "Сидорович",
        "1990-04-04",
        UserProfile.MALE,
        UserProfile.ADMIN,
        company3,
        department6,
        "Менеджер"
    )
    add_user(
        "user4@mail.ru",
        "123456",
        "Васильев",
        "Василий",
        "Васильевич",
        "1990-05-05",
        UserProfile.MALE,
        UserProfile.OPERATOR,
        company1,
        department1,
        "Менеджер"
    )
    add_user(
        "user5@mail.ru",
        "123456",
        "Алексеев",
        "Алексей",
        "Алексеевич",
        "1990-06-06",
        UserProfile.MALE,
        UserProfile.OPERATOR,
        company2,
        department3,
        "Менеджер"
    )
    add_user(
        "user6@mail.ru",
        "123456",
        "Викторов",
        "Виктор",
        "Викторович",
        "1990-07-07",
        UserProfile.MALE,
        UserProfile.OPERATOR,
        company3,
        department5,
        "Менеджер"
    )
    add_user(
        "user7@mail.ru",
        "123456",
        "Аркадьев",
        "Аркадий",
        "Аркадьевич",
        "1990-08-08",
        UserProfile.MALE,
        UserProfile.PROBATIONER,
        company1,
        department2,
        "Менеджер"
    )
    add_user(
        "user8@mail.ru",
        "123456",
        "Григорьев",
        "Григорий",
        "Григорьевич",
        "1990-09-09",
        UserProfile.MALE,
        UserProfile.PROBATIONER,
        company2,
        department4,
        "Менеджер"
    )
    add_user(
        "user9@mail.ru",
        "123456",
        "Никифоров",
        "Никифор",
        "Никифорович",
        "1990-10-10",
        UserProfile.MALE,
        UserProfile.PROBATIONER,
        company3,
        department6,
        "Менеджер"
    )


def add_company(name):
    company = Company.objects.get_or_create(name=name)[0]
    return company

def add_department(company, name):
    department = Department.objects.get_or_create(company=company, name=name)[0]
    return department


def add_super_user(company, department):
    """
    Creates a superuser
    :return:
    """
    try:
        user = django.contrib.auth.get_user_model().objects.create_superuser(
            email="admin@gmail.com",
            date_of_birth="1990-01-01",
            password="admin",
            first_name="Алексей",
            last_name="Кутепов",
            middle_name="Леонидович",
            gender=UserProfile.MALE,
            user_type=UserProfile.CURATOR,
            company=company,
            department=department,
            position="Разработчик"
        )
        return user
    except:
        print("Impossible to create a superuser.")


def add_user(email, password, last_name, first_name, middle_name, birthday, gender, user_type, company, department, position):
    """
    Creates new user into database
    :param email:
    :param password:
    :param first_name:
    :param middle_name:
    :param last_name:
    :param birthday:
    :param gender
    :param user_type
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
        user_type=user_type,
        company=company,
        department=department,
        position=position
    )
    return user_profile


if __name__ == '__main__':
    print("Starting ASCT population script...")
    populate()
    print("Complete!")