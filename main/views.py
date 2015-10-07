from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from main.models import UserProfile


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