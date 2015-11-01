from datetime import timezone
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from main.models import UserProfile, Company, Department, Journal, Theme, SubTheme, ScheduledTheme, ScheduledSubTheme


@login_required
def test_page(request):
    return render(request, "base.html")


def prepare_curator_page(request):
    user_list = UserProfile.objects.all()
    company_list = Company.objects.all()
    return render(
        request,
        "main/curator_profile.html",
        {
            "user_list": user_list,
            "company_list": company_list
        }
    )


def prepare_admin_page(request):
    user_list = UserProfile.objects.filter(
        Q(user_type=UserProfile.OPERATOR, company=request.user.company) | Q(user_type=UserProfile.PROBATIONER, company=request.user.company)
    )
    return render(
        request,
        "main/admin_profile.html",
        {
            "user_list": user_list,
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


@login_required
def create_journal(request):
    if "save" in request.POST:
        journal = Journal.objects.create(name=request.POST["name"], description=request.POST["description"], owner=request.user)
        return render(request, "main/journal_settings.html", {"journal": journal})
    else:
        return render(request, "main/create_journal.html")


@login_required
def journal_settings(request, id):
    try:
        journal = Journal.objects.get(id=id)
    except:
        return HttpResponseRedirect(reverse("index"))
    theme_list = Theme.objects.filter(journal=journal)
    return render(
        request,
        "main/journal_settings.html",
        {
            "journal": journal,
            "theme_list": theme_list
        }
    )


@login_required
def create_theme(request):
    if "save" in request.POST:
        try:
            journal = Journal.objects.get(id=request.POST["save"])
        except:
            return HttpResponseRedirect(reverse("index"))
        theme = Theme.objects.create(name=request.POST["themeName"], description=request.POST["description"], owner=request.user, journal=journal)
        theme_list = Theme.objects.filter(journal=journal)
        return render(
            request,
            "main/journal_settings.html",
            {
                "journal": journal,
                "theme_list": theme_list
            }
        )
    else:
        return HttpResponseRedirect(reverse("index"))


@login_required
def delete_theme(request, id):
    try:
        theme = Theme.objects.get(id=id)
        journal = Journal.objects.get(id=theme.journal.id)
    except:
        return HttpResponseRedirect(reverse("index"))
    theme.delete()
    theme_list = Theme.objects.filter(journal=journal)
    return render(
            request,
            "main/journal_settings.html",
            {
                "journal": journal,
                "theme_list": theme_list
            }
        )


@login_required
def theme_settings(request, id):
    try:
        theme = Theme.objects.get(id=id)
    except:
        return HttpResponseRedirect(reverse("index"))
    sub_theme_list = SubTheme.objects.filter(parent_theme=theme)
    return render(
        request,
        "main/theme_settings.html",
        {
            "theme": theme,
            "sub_theme_list": sub_theme_list
        }
    )


@login_required
def create_sub_theme(request):
    if "save" in request.POST:
        try:
            theme = Theme.objects.get(id=request.POST["save"])
        except:
            return HttpResponseRedirect(reverse("index"))
        sub_theme = SubTheme.objects.create(
            name=request.POST["subThemeName"],
            description=request.POST["description"],
            owner=request.user,
            parent_theme=theme
        )
        sub_theme_list = SubTheme.objects.filter(parent_theme=theme)
        return render(
            request,
            "main/theme_settings.html",
            {
                "theme": theme,
                "sub_theme_list": sub_theme_list
            }
        )
    else:
        return HttpResponseRedirect(reverse("index"))


@login_required
def delete_sub_theme(request, id):
    try:
        sub_theme = SubTheme.objects.get(id=id)
        theme = Theme.objects.get(id=sub_theme.parent_theme.id)
    except:
        return HttpResponseRedirect(reverse("index"))
    sub_theme.delete()
    sub_theme_list = SubTheme.objects.filter(parent_theme=theme)
    return render(
            request,
            "main/theme_settings.html",
            {
                "theme": theme,
                "sub_theme_list": sub_theme_list
            }
    )


@login_required
def get_user_list_by_theme(request):
    if "id" in request.POST:
        theme = Theme.objects.get(id=request.POST["id"])
        scheduled_theme_list = ScheduledTheme.objects.filter(theme=theme)
        result = {}
        list = []
        for item in scheduled_theme_list:
            list.append({
                "id": item.user.id,
                "fio": item.user.get_full_name(),
                "status": "Назначена",
                "date_from": item.date_from,
                "date_to": item.date_to,
                "progress": 50
            })
        result["user_statistic_list"] = list
        return JsonResponse(result)
    else:
        return JsonResponse({"user_statistic_list": []})


@login_required
def schedule_theme(request, id):
    if "save" in request.POST:
        try:
            theme = Theme.objects.get(id=id)
            user = UserProfile.objects.get(id=request.POST["user"])
        except:
            return HttpResponseRedirect(reverse("index"))
        ScheduledTheme.objects.create(
            date_to=request.POST["dateTo"],
            user=user,
            theme=theme
        )
        sub_theme_list = SubTheme.objects.filter(parent_theme=theme)
        for item in sub_theme_list:
            ScheduledSubTheme.objects.create(
                date_to=request.POST["dateTo"],
                user=user,
                sub_theme=item
            )
        return render(
            request,
            "main/theme_settings.html",
            {
                "theme": theme,
                "sub_theme_list": sub_theme_list
            }
        )
    else:
        return HttpResponseRedirect(reverse("index"))


@login_required
def schedule_theme_to_user(request, id):
    if "save" in request.POST:
        try:
            theme = Theme.objects.get(id=id)
            user = UserProfile.objects.get(id=request.POST["user"])
        except:
            return HttpResponseRedirect(reverse("index"))
        ScheduledTheme.objects.create(
            date_to=request.POST["dateTo"],
            user=user,
            theme=theme
        )
        sub_theme_list = SubTheme.objects.filter(parent_theme=theme)
        for item in sub_theme_list:
            ScheduledSubTheme.objects.create(
                date_to=request.POST["dateTo"],
                user=user,
                sub_theme=item
            )
        return render(
            request,
            "main/user_info.html",
            {"user_data": user}
        )
    else:
        return HttpResponseRedirect(reverse("index"))


@login_required
def get_probationer_list(request):
    if request.user.user_type == UserProfile.CURATOR:
        probationer_list = UserProfile.objects.filter(user_type=UserProfile.PROBATIONER)
        result = {}
        list = []
        for item in probationer_list:
            list.append({
                "id": item.id,
                "name": item.get_full_name()
            })
        result["probationer_list"] = list
        return JsonResponse(result)
    else:
        return JsonResponse({"probationer_list": []})


@login_required
def user_info(request, id):
    try:
        user_data = UserProfile.objects.get(id=id)
    except:
        result = {
            "status": "danger",
            "message": "Пользователь не найден"
            }
        return render(request, "alert.html", result)
    return render(request, "main/user_info.html", {"user_data": user_data})


@login_required
def get_theme_list_by_user(request):
    if "id" in request.POST:
        user = UserProfile.objects.get(id=request.POST["id"])
        scheduled_theme_list = ScheduledTheme.objects.filter(user=user)
        result = {}
        list = []
        for item in scheduled_theme_list:
            list.append({
                "id": item.theme.id,
                "name": item.theme.name,
                "status": "Назначена",
                "date_from": item.date_from,
                "date_to": item.date_to,
                "progress": 50
            })
        result["user_statistic_list"] = list
        return JsonResponse(result)
    else:
        return JsonResponse({"user_statistic_list": []})


@login_required
def get_theme_list_by_journal(request):
    if "id" in request.POST:
        journal = Journal.objects.get(id=request.POST["id"])
        theme_list = Theme.objects.filter(journal=journal)
        result = {}
        list = []
        for item in theme_list:
            list.append({
                "id": item.id,
                "name": item.name,
            })
        result["theme_list"] = list
        return JsonResponse(result)
    else:
        return JsonResponse({"theme_list": []})


@login_required
def delete_journal(request, id):
    try:
        journal = Journal.objects.get(id=id)
    except:
        return HttpResponseRedirect(reverse("index"))
    name = journal.name
    journal.delete()
    result = {
            "status": "success",
            "message": "Журнал " + name + " успешно удалён!"
        }
    return render(request, "alert.html", result)