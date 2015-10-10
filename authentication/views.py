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
from main.models import UserProfile
import imghdr


def generate_password(size=8, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


@csrf_protect
def login(request):
    if "email" in request.POST and "password" in request.POST:
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = auth.authenticate(email=email, password=password)
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
    user_data = UserProfile.objects.get(id=id)
    result = {"user_data": user_data}
    if "save" in request.POST:
        if "photo" in request.FILES:
            photo = request.FILES["photo"]
        else:
            photo = None
        if photo and imghdr.what(photo):
            user_data.photo = photo
        user_data.email = request.POST["email"]
        user_data.last_name = request.POST["lastName"]
        user_data.first_name = request.POST["firstName"]
        user_data.middle_name = request.POST["middleName"]
        user_data.date_of_birth = request.POST["dateOfBirth"]
        user_data.gender = request.POST["gender"]
        user_data.company = request.POST["company"]
        user_data.department = request.POST["department"]
        user_data.position = request.POST["position"]
        if "userType" in request.POST:
            user_data.user_type = request.POST["userType"]
        user_data.save()
        result["show_alert_success"] = True
        request["message"] = "Изменения сохранены"
    return render(request, "authentication/user_settings.html", result)


@login_required
def create_new_user(request):
    if "create" in request.POST:
        email = request.POST["email"]
        try:
            user_profile_in_db = UserProfile.objects.get(email=email)
            if user_profile_in_db:
                pass
                # return HttpResponseRedirect(reverse("authentication_alert", args=["danger", "Пользователь с e-mail адресом "+email+" уже существует!"]))
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
        user = auth.get_user_model().objects.create_user(
            email=email,
            password=password,
            date_of_birth=request.POST["dateOfBirth"],
            last_name=request.POST["lastName"],
            first_name=request.POST["firstName"],
            middle_name=request.POST["middleName"],
            gender=request.POST["gender"],
            company=request.POST["company"],
            department=request.POST["department"],
            position=request.POST["position"],
            user_type=request.POST["userType"],
            photo=photo
        )
        try:
            send_mail(
                'Регистрация в ASCT',
                'Здравствуйте ' + user.first_name + '! \n \n Вы успешно зарегистрированы в сервисе ASCT \n \n Ваш логин: ' + user.email + ' \n Ваш пароль: ' + password,
                getattr(settings, "EMAIL_HOST_USER", None),
                [user.email],
                fail_silently=False
            )
        except:
            pass
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "authentication/create_new_user.html")


@login_required
def give_new_password(request, id):
    if request.user.user_type != UserProfile.ADMIN:
        result = {
            "status": "error",
            "message": "Доступ запрещён"
            }
        return render(request, "alert.html", result)
    else:
        user_data = UserProfile.objects.get(id=id)
        password = generate_password()
        user_data.password = password
        user_data.save()
        try:
            send_mail(
                'Новый пароль доступа в ASCT',
                'Здравствуйте ' + user_data.first_name + '! \n \n Вам выдан новый пароль доступа в ASCT \n \n Ваш логин: ' + user_data.email + ' \n Ваш пароль: ' + password,
                getattr(settings, "EMAIL_HOST_USER", None),
                [user_data.email],
                fail_silently=False
            )
        except:
            pass
        result = {
            "status": "success",
            "message": "<p>Пользователь " + user_data.get_full_name() + " получил новый пароль для доступа в ASCT: " + password + "</p> <p>Пароль отправлен на электронную почту пользователя: " + user_data.email + "</p>"
        }
        return render(request, "alert.html", result)
