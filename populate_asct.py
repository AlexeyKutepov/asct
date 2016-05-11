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
    company1 = add_company("Premier Hotels and Resorts")
    company2 = add_company("Гостиница \"Премьер Палас\"")
    company3 = add_company("Гостиница \"Русь\"")

    department1 = add_department(company1, "Администрация")
    department2 = add_department(company1, "Отдел управления персоналом")
    department3 = add_department(company1, "Отдел стандартизации и качества")
    department4 = add_department(company1, "Центральный отдел продаж")

    department5 = add_department(company2, "Отдел бронирования")
    department6 = add_department(company2, "Отдел продаж")
    department7 = add_department(company2, "Служба приема и размещения")
    department8 = add_department(company2, "Служба гостиничного хозяйства")
    department9 = add_department(company2, "Отдел мероприятий")
    department10 = add_department(company2, "Ресторан")
    department11 = add_department(company2, "Служба безопасности")
    department12 = add_department(company2, "Отдел управления персоналом")

    department13 = add_department(company3, "Отдел бронирования")
    department14 = add_department(company3, "Отдел продаж")
    department15 = add_department(company3, "Служба приема и размещения")
    department16 = add_department(company3, "Служба гостиничного хозяйства")
    department17 = add_department(company3, "Отдел мероприятий")
    department18 = add_department(company3, "Ресторан")
    department19 = add_department(company3, "Служба безопасности")
    department20 = add_department(company3, "Отдел управления персоналом")

    position1 = add_position("Специалист по обучению")
    position2 = add_position("Начальник отдела")
    position3 = add_position("Заместитель начальника отедла")
    position4 = add_position("Начальник отдела стандартизации и качества")
    position5 = add_position("Менеджер")
    position6 = add_position("Разработчик")

    super_user = add_super_user(company1, department1, position6)
    add_user(
        "curator1",
        "curator1@mail.ru",
        "123456",
        "Бондарь",
        "Татьяна",
        "Батьковна",
        "1990-02-02",
        UserProfile.FEMALE,
        UserProfile.CURATOR,
        company1,
        department2,
        position1
    )
    add_user(
        "curator2",
        "curator2@mail.ru",
        "123456",
        "Секисова",
        "Валерия",
        "Батьковна",
        "1990-03-03",
        UserProfile.FEMALE,
        UserProfile.CURATOR,
        company1,
        department4,
        position2
    )
    add_user(
        "curator3",
        "curator3@mail.ru",
        "123456",
        "Сидоров",
        "Виктор",
        "Павлович",
        "1990-04-04",
        UserProfile.MALE,
        UserProfile.CURATOR,
        company3,
        department13,
        position2
    )
    add_user(
        "user1",
        "user1@mail.ru",
        "123456",
        "Худык",
        "Леся",
        "Батьковна",
        "1990-02-02",
        UserProfile.FEMALE,
        UserProfile.ADMIN,
        company2,
        department12,
        position1
    )
    add_user(
        "user2",
        "user2@mail.ru",
        "123456",
        "Нечеса",
        "Ольга",
        "Батьковна",
        "1990-03-03",
        UserProfile.FEMALE,
        UserProfile.ADMIN,
        company3,
        department13,
        position1
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
        UserProfile.ADMIN,
        company3,
        department14,
        position1
    )
    add_user(
        "user4",
        "user4@mail.ru",
        "123456",
        "Метельский",
        "Алексей",
        "Анатольевич",
        "1990-05-05",
        UserProfile.MALE,
        UserProfile.OPERATOR,
        company2,
        department6,
        position2
    )
    add_user(
        "user5",
        "user5@mail.ru",
        "123456",
        "Бородина",
        "Марина",
        "Викторовна",
        "1990-06-06",
        UserProfile.FEMALE,
        UserProfile.OPERATOR,
        company3,
        department15,
        position2
    )
    add_user(
        "user6",
        "user6@mail.ru",
        "123456",
        "Авдеенко",
        "Алексей",
        "Батькович",
        "1990-07-07",
        UserProfile.MALE,
        UserProfile.OPERATOR,
        company2,
        department7,
        position3
    )
    add_user(
        "user7",
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
        position5
    )
    add_user(
        "user8",
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
        position5
    )
    add_user(
        "user9",
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
        position5
    )

    journal1 = add_journal(
        "Производственное обучение",
        "",
        super_user,
        company1
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
        "Сюзерены и вассалы",
        "",
        super_user,
        theme2
    )
    sub_theme9 = add_sub_theme(
        "Делопроизводство и документооборот",
        "",
        super_user,
        theme2
    )

    theme3 = add_theme(
        "Услуги и виды обслуживания в оделе",
        "",
        super_user,
        journal1
    )
    sub_theme10 = add_sub_theme(
        "Что полезное мы делаем для общества, и за что нам платят деньги",
        "",
        super_user,
        theme3
    )
    sub_theme11 = add_sub_theme(
        "Наши конференц-возможности",
        "",
        super_user,
        theme3
    )
    sub_theme12 = add_sub_theme(
        "Деловые мероприятия",
        "",
        super_user,
        theme3
    )
    sub_theme13 = add_sub_theme(
        "Торжественные мероприятия",
        "",
        super_user,
        theme3
    )

    theme4 = add_theme(
        "Стандартыне процедуры обслуживания",
        "",
        super_user,
        journal1
    )
    sub_theme14 = add_sub_theme(
        "Жизненный цикл мероприятия",
        "",
        super_user,
        theme4
    )
    sub_theme15 = add_sub_theme(
        "Помоги закачику купить",
        "",
        super_user,
        theme4
    )
    sub_theme16 = add_sub_theme(
        "Организуй меропритие",
        "",
        super_user,
        theme4
    )
    sub_theme17 = add_sub_theme(
        "Проведи мероприятие",
        "",
        super_user,
        theme4
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
            user_type=UserProfile.CURATOR,
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