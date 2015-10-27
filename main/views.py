from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from main.models import UserProfile, Company, Department, Journal


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
def get_journal_list(request):
    journal_list = Journal.objects.all()
    result_list = []
    for journal in journal_list:
        result_list.append({
            "id": journal.id,
            "name": journal.name,
            "owner": journal.owner.get_full_name()
        })
    return JsonResponse({"journal_list": result_list})



@login_required
def create_new_company(request):
    if request.user.user_type == UserProfile.CURATOR:
        if "company" in request.POST:
            company_list = Company.objects.filter(name=request.POST["company"])
            if company_list:
                result = {
                    "status": "danger",
                    "message": "Компания " + request.POST["company"] + " уже существует!"
                }
                return render(request, "alert.html", result)
            else:
                company = Company.objects.create(name=request.POST["company"])
                if "department" in request.POST:
                    for department in request.POST.getlist("department"):
                        Department.objects.create(name=department, company=company)
                result = {
                    "status": "success",
                    "message": "Компания " + request.POST["company"] + " успешно добавлена!"
                }
                return render(request, "alert.html", result)
        else:
            return render(request, "main/company_settings.html", {"isCreate": True, "title": "Новая компания"})
    else:
        return HttpResponseRedirect(reverse("index"))

@login_required
def edit_company(request, id):
    try:
        company = Company.objects.get(id=id)
    except:
        return HttpResponseRedirect(reverse("index"))
    department_list = Department.objects.filter(company=company)
    return render(
        request,
        "main/company_settings.html",
        {
            "isCreate": False,
            "title": "Редактирование компании",
            "company": company,
            "department_list": department_list
        }
    )

@login_required
def edit_company_save(request):
    if "save" in request.POST:
        try:
            company = Company.objects.get(id=request.POST["companyId"])
        except:
            return HttpResponseRedirect(reverse("index"))
        company.name = request.POST["company"]
        company.save()
        if "department" in request.POST:
            department_list_in_base = Department.objects.filter(company=company)
            department_names = [d.name for d in department_list_in_base]
            for department in request.POST.getlist("department"):
                if department not in department_names:
                    Department.objects.create(name=department, company=company)
            for department in department_list_in_base:
                if department.name not in request.POST.getlist("department"):
                    department.delete()
        result = {
            "status": "success",
            "message": "Изменения успешно сохранены!"
        }
        return render(request, "alert.html", result)

    else:
        return HttpResponseRedirect(reverse("index"))




