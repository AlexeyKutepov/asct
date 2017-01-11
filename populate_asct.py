__author__ = 'Alexey Kutepov'

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'asct.settings')

import django
django.setup()

from django.contrib.auth.models import User
from main.models import Company, Department, Theme, Journal, SubTheme, Position
from authentication.models import UserProfile


def populate():
    """
    Populates the database.
    :return:
    """
    company = add_company("Company")

    department1 = add_department(company, "Администрация")
    department2 = add_department(company, "Бухгалтерия")
    department3 = add_department(company, "Отдел разработки")
    department4 = add_department(company, "Отдел закупки")
    department5 = add_department(company, "Отдел продаж")
    department6 = add_department(company, "ИТ")

    position1 = add_position("Директор")
    position2 = add_position("Начальник отдела")
    position3 = add_position("Заместитель начальника отедла")
    position4 = add_position("Менеджер")
    position5 = add_position("Администратор")
    position6 = add_position("Разработчик")
    position7 = add_position("Рабочий")


    super_user = add_super_user(company, department6, position5)
    add_user(
        "user1",
        "user1@mail.ru",
        "123456",
        "Иванов",
        "Иван",
        "Иванович",
        "1990-02-02",
        UserProfile.MALE,
        UserProfile.OPERATOR,
        company,
        department5,
        position4
    )
    add_user(
        "user2",
        "user2@mail.ru",
        "123456",
        "Петров",
        "Пётр",
        "Петрович",
        "1990-03-03",
        UserProfile.MALE,
        UserProfile.OPERATOR,
        company,
        department5,
        position2
    )
    add_user(
        "user3",
        "user3@mail.ru",
        "123456",
        "Сидоров",
        "Сидор",
        "Сидорович",
        "1990-04-04",
        UserProfile.MALE,
        UserProfile.OPERATOR,
        company,
        department4,
        position3
    )
    add_user(
        "user4",
        "user4@mail.ru",
        "123456",
        "Александров",
        "Александр",
        "Александрович",
        "1990-05-05",
        UserProfile.MALE,
        UserProfile.PROBATIONER,
        company,
        department2,
        position4
    )
    add_user(
        "user5",
        "user5@mail.ru",
        "123456",
        "Викторов",
        "Виктор",
        "Викторович",
        "1990-06-06",
        UserProfile.MALE,
        UserProfile.PROBATIONER,
        company,
        department2,
        position2
    )
    add_user(
        "user6",
        "user6@mail.ru",
        "123456",
        "Сергеев",
        "Сергей",
        "Сергеевич",
        "1990-07-07",
        UserProfile.MALE,
        UserProfile.PROBATIONER,
        company,
        department3,
        position6
    )


    journal1 = add_journal(
        "Производственное обучение",
        "",
        super_user,
        company
    )

    theme1 = add_theme(
        "Выживание на предприятии",
        "",
        super_user,
        journal1
    )
    sub_theme1 = add_sub_theme(
        "Охрана труда",
        "",
        super_user,
        theme1
    )
    sub_theme2 = add_sub_theme(
        "Пожарная безопасность",
        "",
        super_user,
        theme1
    )
    sub_theme3 = add_sub_theme(
        "Санитария на производстве",
        "",
        super_user,
        theme1
    )
    sub_theme4 = add_sub_theme(
        "Безопасность жизнедеятельности на предприятии",
        "",
        super_user,
        theme1
    )
    sub_theme5 = add_sub_theme(
        "Первая медицинская помощь",
        "",
        super_user,
        theme1
    )

    theme2 = add_theme(
        "Ознакомление с подраделением",
        "",
        super_user,
        journal1
    )
    sub_theme6 = add_sub_theme(
        "Режим и график",
        "",
        super_user,
        theme2
    )
    sub_theme7 = add_sub_theme(
        "Кто чем занимается и за что отвечает",
        "",
        super_user,
        theme2
    )
    sub_theme8 = add_sub_theme(
        "Делопроизводство и документооборот",
        "",
        super_user,
        theme2
    )


def add_company(name):
    company = Company.objects.get_or_create(name=name)[0]
    return company


def add_department(company, name):
    department = Department.objects.get_or_create(company=company, name=name)[0]
    return department


def add_position(name):
    position = Position.objects.get_or_create(name=name)[0]
    return position


def add_journal(name, description, owner, company):
    journal = Journal.objects.get_or_create(
        name=name,
        description=description,
        owner=owner,
        company=company
    )[0]
    return journal


def add_theme(name, description, owner, journal):
    theme = Theme.objects.get_or_create(
        name=name,
        description=description,
        owner=owner,
        journal=journal
    )[0]
    return theme


def add_sub_theme(name, description, owner, parent_theme):
    sub_theme = SubTheme.objects.get_or_create(
        name=name,
        description=description,
        owner=owner,
        parent_theme=parent_theme
    )[0]
    return sub_theme


def add_super_user(company, department, position):
    """
    Creates a superuser
    :return:
    """
    try:
        user = django.contrib.auth.get_user_model().objects.create_superuser(
            username="admin",
            email="admin@gmail.com",
            date_of_birth="1990-01-01",
            password="admin",
            first_name="Алексей",
            last_name="Кутепов",
            middle_name="Леонидович",
            gender=UserProfile.MALE,
            user_type=UserProfile.ADMIN,
            company=company,
            department=department,
            position=position
        )
        return user
    except:
        print("Impossible to create a superuser.")


def add_user(username, email, password, last_name, first_name, middle_name, birthday, gender, user_type, company, department, position):
    """
    Creates new user into database
    :param username
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
        username=username,
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