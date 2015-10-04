from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from main.models import UserProfile


@login_required
def index(request):
    if request.user.user_type == UserProfile.ADMIN:
        return render(request, "main/admin_profile.html")
    elif request.user.user_type == UserProfile.OPERATOR:
        return render(request, "main/operator_profile.html")
    elif request.user.user_type == UserProfile.PROBATIONER:
        return render(request, "main/probationer_profile.html")
    return render(request, "base.html")