from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from main.models import UserProfile
import imghdr


@login_required
def test_page(request):
    return render(request, "base.html")


@login_required
def index(request):
    if request.user.user_type == UserProfile.ADMIN:
        admin_list = UserProfile.objects.filter(user_type=UserProfile.ADMIN)
        operator_list = UserProfile.objects.filter(user_type=UserProfile.OPERATOR)
        probationer_list = UserProfile.objects.filter(user_type=UserProfile.PROBATIONER)
        return render(
            request,
            "main/admin_profile.html",
            {
                "admin_list": admin_list,
                "operator_list": operator_list,
                "probationer_list": probationer_list,
            }
        )
    elif request.user.user_type == UserProfile.OPERATOR:
        probationer_list = UserProfile.objects.filter(user_type=UserProfile.PROBATIONER)
        return render(
            request,
            "main/operator_profile.html",
            {
                "probationer_list": probationer_list,
            }
        )
    elif request.user.user_type == UserProfile.PROBATIONER:
        return render(request, "main/probationer_profile.html")
    else:
        return render(request, "base.html")


@login_required
def user_settings(request, id):
    user_data = UserProfile.objects.get(id=id)
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

    return render(request, "main/user_settings.html", {"user_data": user_data})