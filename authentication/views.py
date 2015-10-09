from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from main.models import UserProfile
import imghdr


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

    return render(request, "authentication/user_settings.html", result)
