from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from main.models import UserProfile, Company, Department


@login_required
def test_page(request):
    return render(request, "base.html")


def prepare_curator_page(request):
    curator_list = UserProfile.objects.filter(user_type=UserProfile.CURATOR)
    admin_list = UserProfile.objects.filter(user_type=UserProfile.ADMIN)
    operator_list = UserProfile.objects.filter(user_type=UserProfile.OPERATOR)
    probationer_list = UserProfile.objects.filter(user_type=UserProfile.PROBATIONER)
    company_list = Company.objects.all()
    return render(
        request,
        "main/curator_profile.html",
        {
            "curator_list": curator_list,
            "admin_list": admin_list,
            "operator_list": operator_list,
            "probationer_list": probationer_list,
            "company_list": company_list
        }
    )


def prepare_admin_page(request):
    admin_list = UserProfile.objects.filter(user_type=UserProfile.ADMIN, company=request.user.company)
    operator_list = UserProfile.objects.filter(user_type=UserProfile.OPERATOR, company=request.user.company)
    probationer_list = UserProfile.objects.filter(user_type=UserProfile.PROBATIONER, company=request.user.company)
    return render(
        request,
        "main/admin_profile.html",
        {
            "admin_list": admin_list,
            "operator_list": operator_list,
            "probationer_list": probationer_list,
        }
    )


def prepare_operator_page(request):
    probationer_list = UserProfile.objects.filter(user_type=UserProfile.PROBATIONER, company=request.user.company)
    return render(
        request,
        "main/operator_profile.html",
        {
            "probationer_list": probationer_list,
        }
    )


def prepare_probationer_page(request):
    return render(request, "main/probationer_profile.html")


@login_required
def index(request):
    if request.user.user_type == UserProfile.CURATOR:
        return prepare_curator_page(request)
    elif request.user.user_type == UserProfile.ADMIN:
        return prepare_admin_page(request)
    elif request.user.user_type == UserProfile.OPERATOR:
        return prepare_operator_page(request)
    elif request.user.user_type == UserProfile.PROBATIONER:
        return prepare_probationer_page(request)
    else:
        return render(request, "base.html")


@login_required
def get_department_list(request):
    if "id" in request.POST:
        company = Company.objects.get(id=request.POST["id"])
        department_list = Department.objects.filter(company=company)
        result = {}
        list = []
        for department in department_list:
            list.append({
                "id": department.id,
                "name": department.name
            })
        result["department_list"] = list
        return JsonResponse(result)
    else:
        return JsonResponse({"department_list": []})


@login_required
def get_user_list_by_department(request):
    if "id" in request.POST:
        department = Department.objects.get(id=request.POST["id"])
        user_list = UserProfile.objects.filter(department=department)
        result = {}
        list = []
        for user in user_list:
            list.append({
                "id": user.id,
                "name": user.get_full_name()
            })
        result["user_list"] = list
        return JsonResponse(result)
    else:
        return JsonResponse({"user_list": []})


@login_required
def create_new_company(request):
    if request.user.user_type == UserProfile.CURATOR:
        return render(request, "main/company_settings.html", {"title": "Новая компания"})
    else:
        return HttpResponseRedirect(reverse("index"))


