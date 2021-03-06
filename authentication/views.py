import datetime
import random
import string
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from asct import settings
from main.models import Company, Department, Position
from authentication.models import UserProfile
import imghdr


def generate_password(size=8, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


@csrf_protect
def login(request):
    if "username" in request.POST and "password" in request.POST:
        username = str(request.POST.get("username")).strip()
        password = str(request.POST.get("password")).strip()
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "authentication/login.html", {"login_error": "has-error"})
    else:
        return render(request, "authentication/login.html")


@login_required(login_url='/')
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse("index"))


@login_required
def user_settings(request, id):
    try:
        user_data = UserProfile.objects.get(id=id)
    except:
        result = {
            "status": "danger",
            "message": "Пользователь не найден"
        }
        return render(request, "alert.html", result)
    department_list = Department.objects.all()
    position_list = Position.objects.all()
    if "save" in request.POST:
        if "photo" in request.FILES:
            photo = request.FILES["photo"]
        else:
            photo = None
        if photo and imghdr.what(photo):
            user_data.photo = photo
        user_data.username = request.POST["username"]
        user_data.email = request.POST["email"]
        user_data.last_name = request.POST["lastName"]
        user_data.first_name = request.POST["firstName"]
        user_data.middle_name = request.POST["middleName"]
        user_data.date_of_birth = datetime.datetime.strptime(request.POST["dateOfBirth"], "%d.%m.%Y")
        user_data.gender = request.POST["gender"]
        user_data.company = Company.objects.get_or_create(id=1)[0]
        if "department" in request.POST:
            department = Department.objects.get(id=request.POST["department"])
            user_data.department = department
        if "position" in request.POST:
            position = Position.objects.get(id=request.POST["position"])
            user_data.position = position
        else:
            user_data.position = None
        if "userType" in request.POST:
            user_data.user_type = request.POST["userType"]
        user_data.save()

        return render(
            request,
            "alert.html",
            {
                "status": "success",
                "message": "Изменения профиля пользователя успешно сохранены! Профиль пользователя: <a href=\"" + request.META.get(
                    'HTTP_REFERER') + "\">" + user_data.get_full_name() + "</a>"
            }
        )
    else:
        return render(
            request,
            "authentication/user_settings.html",
            {
                "user_data": user_data,
                "department_list": department_list,
                "position_list": position_list,
                "isCreate": False
            }
        )


@login_required
def create_new_user(request):
    if "create" in request.POST:
        username = request.POST["username"]
        try:
            user_profile_in_db = UserProfile.objects.get(username=username)
            if user_profile_in_db:
                return render(
                    request,
                    "alert.html",
                    {
                        "status": "danger",
                        "message": "Пользователь " + username + " уже существует!"
                    }
                )
        except:
            # Exception does not matter
            pass
        if "photo" in request.FILES:
            photo = request.FILES["photo"]
        else:
            photo = None
        if photo and not imghdr.what(photo):
            photo = None
        password = generate_password()
        if "userType" in request.POST:
            user_type = request.POST["userType"]
        else:
            user_type = UserProfile.PROBATIONER
        if "department" in request.POST:
            department = Department.objects.get(id=request.POST["department"])
        else:
            department = None
        if "position" in request.POST:
            position = Position.objects.get(id=request.POST["position"])
        else:
            position = None
        user = auth.get_user_model().objects.create_user(
            username=username,
            email=request.POST["email"],
            password=password,
            date_of_birth=datetime.datetime.strptime(request.POST["dateOfBirth"], "%d.%m.%Y"),
            last_name=request.POST["lastName"],
            first_name=request.POST["firstName"],
            middle_name=request.POST["middleName"],
            gender=request.POST["gender"],
            company=Company.objects.get_or_create(id=1)[0],
            department=department,
            position=position,
            user_type=user_type,
            photo=photo
        )
        try:
            send_mail(
                'Регистрация в E-ducation Hub',
                'Здравствуйте ' + user.first_name + '! \n \nВы успешно зарегистрированы в сервисе E-ducation Hub \n \nВаш логин: ' + user.username + ' \nВаш пароль: ' + password +
                ' \n\nДля авторизации в системе перейдите по ссылке: ' + "http://" + request.get_host(),
                getattr(settings, "EMAIL_HOST_USER", None),
                [user.email],
                fail_silently=False
            )
        except:
            pass
        result = {
            "status": "success",
            "message": "<p>Пользователь " + user.get_full_name() + " успешно добавлен в систему</p> <p>Логин и пароль для доступа в E-ducation Hub отправлены на электронную почту пользователя: " + user.email + "</p>"
        }
        return render(request, "alert.html", result)
    else:
        department_list = Department.objects.all()
        position_list = Position.objects.all()
        return render(
            request,
            "authentication/user_settings.html",
            {
                "department_list": department_list,
                "position_list": position_list,
                "isCreate": True
            }
        )


@login_required
def give_new_password(request, id):
    if request.user.user_type != UserProfile.ADMIN:
        result = {
            "status": "danger",
            "message": "Доступ запрещён"
        }
        return render(request, "alert.html", result)
    else:
        try:
            user_data = UserProfile.objects.get(id=id)
        except:
            result = {
                "status": "danger",
                "message": "Пользователь не найден"
            }
            return render(request, "alert.html", result)
        password = generate_password()
        user_data.set_password(password)
        user_data.save()
        try:
            send_mail(
                'Новый пароль доступа в E-ducation Hub',
                'Здравствуйте ' + user_data.first_name + '! \n \nВам выдан новый пароль доступа в E-ducation Hub \n \nВаш логин: ' + user_data.username + ' \nВаш пароль: ' + password +
                ' \n\nДля авторизации в системе перейдите по ссылке: ' + "http://" + request.get_host(),
                getattr(settings, "EMAIL_HOST_USER", None),
                [user_data.email],
                fail_silently=False
            )
        except:
            pass
        result = {
            "status": "success",
            "message": "<p>Пользователь <a href=\"" + request.META.get('HTTP_REFERER') + "\">"
                       + user_data.get_full_name() + "</a> получил новый пароль для доступа в E-ducation Hub.</p> <p>Пароль отправлен на электронную почту пользователя: " + user_data.email + "</p>"
        }
        return render(request, "alert.html", result)


@login_required
def delete_user(request, id):
    if request.user.user_type == UserProfile.PROBATIONER:
        result = {
            "status": "danger",
            "message": "Доступ запрещён"
        }
        return render(request, "alert.html", result)
    else:
        try:
            user_data = UserProfile.objects.get(id=id)
        except:
            result = {
                "status": "danger",
                "message": "Пользователь не найден"
            }
            return render(request, "alert.html", result)
        full_name = user_data.get_full_name()
        user_data.delete()
        result = {
            "status": "success",
            "message": "<p>Пользователь " + full_name + " удалён</p>"
        }
        return render(request, "alert.html", result)


def fire_user(request, id):
    if request.user.user_type == UserProfile.PROBATIONER:
        result = {
            "status": "danger",
            "message": "Доступ запрещён"
        }
        return render(request, "alert.html", result)
    else:
        try:
            user_data = UserProfile.objects.get(id=id)
        except:
            result = {
                "status": "danger",
                "message": "Пользователь не найден"
            }
            return render(request, "alert.html", result)
        full_name = user_data.get_full_name()
        user_data.is_active = False
        user_data.save()
        result = {
            "status": "success",
            "message": "<p>Пользователь <a href=\"" + request.META.get('HTTP_REFERER') + "\">"  + full_name + "</a>  уволен</p>"
        }
        return render(request, "alert.html", result)


def hire_user(request, id):
    if request.user.user_type == UserProfile.PROBATIONER:
        result = {
            "status": "danger",
            "message": "Доступ запрещён"
        }
        return render(request, "alert.html", result)
    else:
        try:
            user_data = UserProfile.objects.get(id=id)
        except:
            result = {
                "status": "danger",
                "message": "Пользователь не найден"
            }
            return render(request, "alert.html", result)
        full_name = user_data.get_full_name()
        user_data.is_active = True
        user_data.save()
        result = {
            "status": "success",
            "message": "<p>Пользователь <a href=\"" + request.META.get('HTTP_REFERER') + "\">"  + full_name + "</a> принят на работу</p>"
        }
        return render(request, "alert.html", result)