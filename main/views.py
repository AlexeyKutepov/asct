from datetime import timezone
from wsgiref.util import FileWrapper
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from main.models import UserProfile, Company, Department, Journal, Theme, SubTheme, ScheduledTheme, ScheduledSubTheme, \
    File, Position, ThemeExam


@login_required
def test_page(request):
    return render(request, "base.html")


def prepare_curator_page(request):
    user_list = UserProfile.objects.all()
    company_list = Company.objects.all()
    position_list = Position.objects.all()
    return render(
        request,
        "main/curator_profile.html",
        {
            "user_list": user_list,
            "company_list": company_list,
            "position_list": position_list
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
    scheduled_theme_list = ScheduledTheme.objects.filter(user=request.user)
    return render(request, "main/probationer_profile.html", {"scheduled_theme_list": scheduled_theme_list})


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
    if request.user.user_type == UserProfile.CURATOR:
        journal_list = Journal.objects.all()
    elif request.user.user_type == UserProfile.ADMIN or request.user.user_type == UserProfile.OPERATOR:
        journal_list = Journal.objects.filter(Q(company=request.user.company) | Q(company=None))
    else:
        journal_list = []
    result_list = []
    for journal in journal_list:
        company = journal.company.name if journal.company else ""
        result_list.append({
            "id": journal.id,
            "name": journal.name,
            "company": company
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
        result = {
            "status": "danger",
            "message": "Доступ запрещён"
            }
        return render(request, "alert.html", result)


@login_required
def edit_company(request, id):
    if request.user.user_type == UserProfile.PROBATIONER:
        result = {
            "status": "danger",
            "message": "Доступ запрещён"
            }
        return render(request, "alert.html", result)
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
    if request.user.user_type == UserProfile.PROBATIONER:
        result = {
            "status": "danger",
            "message": "Доступ запрещён"
            }
        return render(request, "alert.html", result)
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
                    # ВАЖНЫЙ МОМЕНТ: перед удалением департамента нужно почистить юзеров от него, иначе они будут удалены
                    user_list = UserProfile.objects.filter(department=department)
                    for item in user_list:
                        item.department = None
                        item.save()
                    department.delete()
        else:
            department_list_in_base = Department.objects.filter(company=company)
            for department in department_list_in_base:
                # ВАЖНЫЙ МОМЕНТ: перед удалением департамента нужно почистить юзеров от него, иначе они будут удалены
                    user_list = UserProfile.objects.filter(department=department)
                    for item in user_list:
                        item.department = None
                        item.save()
                    department.delete()
        result = {
            "status": "success",
            "message": "Изменения успешно сохранены!"
        }
        return render(request, "alert.html", result)

    else:
        return HttpResponseRedirect(reverse("index"))


@login_required
def delete_company(request, id):
    if request.user.user_type == UserProfile.PROBATIONER:
        result = {
            "status": "danger",
            "message": "Доступ запрещён"
            }
        return render(request, "alert.html", result)
    try:
        company = Company.objects.get(id=id)
    except:
        return HttpResponseRedirect(reverse("index"))
    name = company.name
    user_list = UserProfile.objects.filter(company=company)
    for item in user_list:
        item.company = None
        item.department = None
        item.save()
    company.delete()
    result = {
            "status": "success",
            "message": "Компания \"" + name + "\" удалена!"
        }
    return render(request, "alert.html", result)


@login_required
def create_journal(request):
    if request.user.user_type == UserProfile.PROBATIONER:
        result = {
            "status": "danger",
            "message": "Доступ запрещён"
            }
        return render(request, "alert.html", result)
    if "save" in request.POST:
        if "company" in request.POST:
            try:
                company = Company.objects.get(id=request.POST["company"])
            except:
                company = request.user.company
        else:
            company = request.user.company
        journal = Journal.objects.create(
            name=request.POST["name"],
            description=request.POST["description"],
            owner=request.user,
            company=company
        )
        return HttpResponseRedirect(reverse("journal_settings", args=[journal.id, ]))
    else:
        if request.user.user_type == UserProfile.CURATOR:
            company_list = Company.objects.all()
        else:
            company_list = []
        return render(request, "main/create_journal.html", {"company_list": company_list})


@login_required
def edit_journal(request, id):
    if request.user.user_type == UserProfile.PROBATIONER:
        result = {
            "status": "danger",
            "message": "Доступ запрещён"
            }
        return render(request, "alert.html", result)
    try:
        journal = Journal.objects.get(id=id)
    except:
        return HttpResponseRedirect(reverse("index"))
    if "name" in request.POST:
        journal.name = request.POST["name"]
    if "description" in request.POST:
        journal.description = request.POST["description"]
    if "company" in request.POST:
        try:
            company = Company.objects.get(id=request.POST["company"])
            journal.company = company
        except:
            pass
    journal.save()
    return HttpResponseRedirect(reverse("journal_settings", args=[journal.id,]))


@login_required
def clone_journal(request, id):
    if request.user.user_type == UserProfile.PROBATIONER:
        result = {
            "status": "danger",
            "message": "Доступ запрещён"
        }
        return render(request, "alert.html", result)
    try:
        journal = Journal.objects.get(id=id)
    except:
        return HttpResponseRedirect(reverse("index"))
    if "company" in request.POST:
        try:
            company = Company.objects.get(id=request.POST["company"])
        except:
            company = request.user.company
    else:
        company = request.user.company
    cloned_journal = Journal.objects.create(
        name=journal.name,
        description=journal.description,
        owner=request.user,
        company=company
    )
    theme_list = Theme.objects.filter(journal=journal)
    for theme in theme_list:
        cloned_theme = Theme.objects.create(
            name=theme.name,
            description=theme.description,
            owner=request.user,
            journal=cloned_journal
        )
        sub_theme_list = SubTheme.objects.filter(parent_theme=theme)
        for sub_theme in sub_theme_list:
            cloned_sub_theme = SubTheme.objects.create(
                name=sub_theme.name,
                description=sub_theme.description,
                owner=request.user,
                parent_theme=cloned_theme
            )
    result = {
        "status": "success",
        "message": "Журнал \"" + journal.name + "\" дублирован для компании \"" + company.name + "\""
    }
    return render(request, "alert.html", result)


@login_required
def journal_settings(request, id):
    if request.user.user_type == UserProfile.PROBATIONER:
        result = {
            "status": "danger",
            "message": "Доступ запрещён"
            }
        return render(request, "alert.html", result)
    try:
        journal = Journal.objects.get(id=id)
    except:
        return HttpResponseRedirect(reverse("index"))
    theme_list = Theme.objects.filter(journal=journal)
    if request.user.user_type == UserProfile.CURATOR:
        company_list = Company.objects.all()
    else:
        company_list = []
    return render(
        request,
        "main/journal_settings.html",
        {
            "journal": journal,
            "theme_list": theme_list,
            "company_list": company_list
        }
    )


@login_required
def create_theme(request):
    if request.user.user_type == UserProfile.PROBATIONER:
        result = {
            "status": "danger",
            "message": "Доступ запрещён"
            }
        return render(request, "alert.html", result)
    if "save" in request.POST:
        try:
            journal = Journal.objects.get(id=request.POST["save"])
        except:
            return HttpResponseRedirect(reverse("index"))
        theme = Theme.objects.create(
            name=request.POST["themeName"],
            description=request.POST["description"],
            owner=request.user,
            journal=journal
        )
        return HttpResponseRedirect(reverse("journal_settings", args=[journal.id,]))
    else:
        return HttpResponseRedirect(reverse("index"))


@login_required
def delete_theme(request, id):
    if request.user.user_type == UserProfile.PROBATIONER:
        result = {
            "status": "danger",
            "message": "Доступ запрещён"
            }
        return render(request, "alert.html", result)
    try:
        theme = Theme.objects.get(id=id)
        journal = Journal.objects.get(id=theme.journal.id)
    except:
        return HttpResponseRedirect(reverse("index"))
    theme.delete()
    return HttpResponseRedirect(reverse("journal_settings", args=[journal.id,]))



@login_required
def theme_settings(request, id):
    if request.user.user_type == UserProfile.PROBATIONER:
        result = {
            "status": "danger",
            "message": "Доступ запрещён"
            }
        return render(request, "alert.html", result)
    try:
        theme = Theme.objects.get(id=id)
    except:
        return HttpResponseRedirect(reverse("index"))
    sub_theme_list = SubTheme.objects.filter(parent_theme=theme)
    if request.user.user_type == UserProfile.CURATOR:
        scheduled_theme_list = ScheduledTheme.objects.filter(theme=theme)
    else:
        user_list = UserProfile.objects.filter(company=request.user.company)
        scheduled_theme_list = ScheduledTheme.objects.filter(theme=theme, user__in=user_list)
    exam_list = ThemeExam.objects.filter(theme=theme)
    file_dict = {}
    for sub_theme in sub_theme_list:
        try:
            file = File.objects.filter(sub_theme=sub_theme)[0]
        except:
            continue
        file_dict[sub_theme.id] = file.id
    return render(
        request,
        "main/theme_settings.html",
        {
            "theme": theme,
            "sub_theme_list": sub_theme_list,
            "file_dict": file_dict,
            "scheduled_theme_list": scheduled_theme_list,
            "exam_list": exam_list
        }
    )


@login_required
def create_sub_theme(request):
    if request.user.user_type == UserProfile.PROBATIONER:
        result = {
            "status": "danger",
            "message": "Доступ запрещён"
            }
        return render(request, "alert.html", result)
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
        return HttpResponseRedirect(reverse("theme_settings", args=[theme.id,]))
    else:
        return HttpResponseRedirect(reverse("index"))


@login_required
def delete_sub_theme(request, id):
    if request.user.user_type == UserProfile.PROBATIONER:
        result = {
            "status": "danger",
            "message": "Доступ запрещён"
            }
        return render(request, "alert.html", result)
    try:
        sub_theme = SubTheme.objects.get(id=id)
        theme = Theme.objects.get(id=sub_theme.parent_theme.id)
    except:
        return HttpResponseRedirect(reverse("index"))
    sub_theme.delete()
    return HttpResponseRedirect(reverse("theme_settings", args=[theme.id,]))


@login_required
def get_user_list_by_theme(request):
    if "id" in request.POST:
        theme = Theme.objects.get(id=request.POST["id"])
        scheduled_theme_list = ScheduledTheme.objects.filter(theme=theme)
        result = {}
        list = []
        for item in scheduled_theme_list:
            if item.status == ScheduledTheme.ASSIGNED:
                progress = 0
                status = "Назначена"
            elif item.status == ScheduledTheme.COMPLETED:
                progress = 100
                status = "Тема изучена"
            else:
                progress = 50
                status = "Изучение"
            list.append({
                "id": item.user.id,
                "fio": item.user.get_full_name(),
                "status": status,
                "date_from": item.date_from,
                "date_to": item.date_to,
                "progress": progress
            })
        result["user_statistic_list"] = list
        return JsonResponse(result)
    else:
        return JsonResponse({"user_statistic_list": []})


@login_required
def schedule_theme(request, id):
    if request.user.user_type == UserProfile.PROBATIONER:
        result = {
            "status": "danger",
            "message": "Доступ запрещён"
            }
        return render(request, "alert.html", result)
    if "save" in request.POST:
        try:
            theme = Theme.objects.get(id=id)
            user = UserProfile.objects.get(id=request.POST["user"])
        except:
            return HttpResponseRedirect(reverse("index"))
        scheduled_theme = ScheduledTheme.objects.create(
            date_to=request.POST["dateTo"],
            user=user,
            theme=theme
        )
        sub_theme_list = SubTheme.objects.filter(parent_theme=theme)
        for item in sub_theme_list:
            ScheduledSubTheme.objects.create(
                date_to=request.POST["dateTo"],
                user=user,
                sub_theme=item,
                scheduled_theme=scheduled_theme
            )
        return HttpResponseRedirect(reverse("theme_settings", args=[theme.id,]))
    else:
        return HttpResponseRedirect(reverse("index"))


@login_required
def schedule_theme_to_user(request):
    if request.user.user_type == UserProfile.PROBATIONER:
        result = {
            "status": "danger",
            "message": "Доступ запрещён"
            }
        return render(request, "alert.html", result)
    if "save" in request.POST:
        try:
            theme = Theme.objects.get(id=request.POST["theme"])
            user = UserProfile.objects.get(id=request.POST["user"])
        except:
            return HttpResponseRedirect(reverse("index"))
        scheduled_theme = ScheduledTheme.objects.create(
            date_to=request.POST["dateTo"],
            user=user,
            theme=theme
        )
        sub_theme_list = SubTheme.objects.filter(parent_theme=theme)
        for item in sub_theme_list:
            ScheduledSubTheme.objects.create(
                date_to=request.POST["dateTo"],
                user=user,
                sub_theme=item,
                scheduled_theme=scheduled_theme
            )
        return HttpResponseRedirect(reverse("user_info", args=[user.id,]))
    else:
        return HttpResponseRedirect(reverse("index"))


@login_required
def schedule_exam(request, id):
    if request.user.user_type == UserProfile.PROBATIONER:
        result = {
            "status": "danger",
            "message": "Доступ запрещён"
            }
        return render(request, "alert.html", result)
    if "save" in request.POST:
        try:
            theme = Theme.objects.get(id=id)
            user = UserProfile.objects.get(id=request.POST["user"])
            examiner = UserProfile.objects.get(id=request.POST["examiner"])
        except:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        theme_exam = ThemeExam.objects.create(
            user=user,
            examiner=examiner,
            theme=theme,
            datetime=request.POST["datetime"],
            place=request.POST["place"],
        )
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def get_probationer_list(request):
    if request.user.user_type != UserProfile.PROBATIONER and "themeId" in request.POST:
        try:
            theme = Theme.objects.get(id=request.POST["themeId"])
        except:
            theme = None
        if theme:
            probationer_list = UserProfile.objects.filter(user_type=UserProfile.PROBATIONER, company=theme.journal.company)
        else:
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
def get_examiner_list(request):
    if request.user.user_type != UserProfile.PROBATIONER and "themeId" in request.POST:
        try:
            theme = Theme.objects.get(id=request.POST["themeId"])
        except:
            theme = None
        if theme:
            examiner_list = UserProfile.objects.filter(~Q(user_type=UserProfile.PROBATIONER), company=theme.journal.company)
        else:
            examiner_list = UserProfile.objects.filter(~Q(user_type=UserProfile.PROBATIONER))
        result = {}
        list = []
        for item in examiner_list:
            list.append({
                "id": item.id,
                "name": item.get_full_name()
            })
        result["examiner_list"] = list
        return JsonResponse(result)
    else:
        return JsonResponse({"examiner_list": []})


@login_required
def user_info(request, id):
    if request.user.user_type == UserProfile.PROBATIONER:
        result = {
            "status": "danger",
            "message": "Доступ запрещён"
            }
        return render(request, "alert.html", result)
    try:
        user_data = UserProfile.objects.get(id=id)
    except:
        result = {
            "status": "danger",
            "message": "Пользователь не найден"
            }
        return render(request, "alert.html", result)
    scheduled_theme_list = ScheduledTheme.objects.filter(user=user_data)
    return render(
        request,
        "main/user_info.html",
        {
            "user_data": user_data,
            "scheduled_theme_list": scheduled_theme_list
        }
    )


@login_required
def get_theme_list_by_user(request):
    if "id" in request.POST:
        user = UserProfile.objects.get(id=request.POST["id"])
        scheduled_theme_list = ScheduledTheme.objects.filter(user=user)
        result = {}
        list = []
        for item in scheduled_theme_list:
            if item.status == ScheduledTheme.ASSIGNED:
                status = "Назначена"
            elif item.status == ScheduledTheme.COMPLETED:
                status = "Тема изучена"
            else:
                status = "Изучение"
            list.append({
                "id": item.theme.id,
                "name": item.theme.name,
                "status": status,
                "date_from": item.date_from,
                "date_to": item.date_to,
                "progress": item.progress
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
    if request.user.user_type == UserProfile.PROBATIONER:
        result = {
            "status": "danger",
            "message": "Доступ запрещён"
            }
        return render(request, "alert.html", result)
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


@login_required
def probationer_theme_settings(request, id):
    try:
        scheduled_theme = ScheduledTheme.objects.get(id=id)
    except:
        return HttpResponseRedirect(reverse("index"))
    sub_theme_list = SubTheme.objects.filter(parent_theme=scheduled_theme.theme)
    scheduled_sub_theme_list = ScheduledSubTheme.objects.filter(sub_theme__in=sub_theme_list, user=request.user, scheduled_theme=scheduled_theme)
    file_dict = {}
    for sub_theme in sub_theme_list:
        try:
            file = File.objects.filter(sub_theme=sub_theme)[0]
        except:
            continue
        file_dict[sub_theme.id] = file.id
    return render(
        request,
        "main/probationer_theme_settings.html",
        {
            "scheduled_theme": scheduled_theme,
            "scheduled_sub_theme_list": scheduled_sub_theme_list,
            "file_dict": file_dict
        }
    )


@login_required
def theme_in_work(request, id):
    try:
        scheduled_theme = ScheduledTheme.objects.get(id=id)
    except:
        return HttpResponseRedirect(reverse("index"))
    scheduled_theme.status = ScheduledTheme.IN_WORK
    scheduled_theme.save()
    return HttpResponseRedirect(reverse("probationer_theme_settings", args=[id,]))


@login_required
def theme_completed(request, id):
    try:
        scheduled_theme = ScheduledTheme.objects.get(id=id)
    except:
        return HttpResponseRedirect(reverse("index"))
    scheduled_sub_theme_list = ScheduledSubTheme.objects.filter(scheduled_theme=scheduled_theme)
    for item in scheduled_sub_theme_list:
        item.status = ScheduledSubTheme.COMPLETED
        item.save()
    scheduled_theme.status = ScheduledTheme.COMPLETED
    scheduled_theme.progress = 100
    scheduled_theme.save()
    return HttpResponseRedirect(reverse("probationer_theme_settings", args=[id,]))


@login_required
def sub_theme_in_work(request, id):
    try:
        scheduled_sub_theme = ScheduledSubTheme.objects.get(id=id)
    except:
        return HttpResponseRedirect(reverse("index"))
    scheduled_sub_theme.status = ScheduledSubTheme.IN_WORK
    scheduled_sub_theme.save()
    return HttpResponseRedirect(reverse("probationer_theme_settings", args=[scheduled_sub_theme.scheduled_theme.id,]))


@login_required
def sub_theme_completed(request, id):
    try:
        scheduled_sub_theme = ScheduledSubTheme.objects.get(id=id)
    except:
        return HttpResponseRedirect(reverse("index"))
    scheduled_sub_theme.status = ScheduledSubTheme.COMPLETED
    scheduled_sub_theme.save()

    scheduled_sub_theme_list = ScheduledSubTheme.objects.filter(scheduled_theme=scheduled_sub_theme.scheduled_theme)
    scheduled_sub_theme_list_completed = ScheduledSubTheme.objects.filter(scheduled_theme=scheduled_sub_theme.scheduled_theme, status=ScheduledSubTheme.COMPLETED)
    scheduled_sub_theme.scheduled_theme.progress = int((100 / len(scheduled_sub_theme_list)) * len(scheduled_sub_theme_list_completed))
    scheduled_sub_theme.scheduled_theme.save()
    return HttpResponseRedirect(reverse("probationer_theme_settings", args=[scheduled_sub_theme.scheduled_theme.id,]))


@login_required
def upload_file_to_sub_theme(request):
    if "subThemeId" in request.POST:
        try:
            sub_theme = SubTheme.objects.get(id=request.POST["subThemeId"])
        except:
            return HttpResponseRedirect(reverse("index"))
        file = File.objects.filter(sub_theme=sub_theme)
        if len(file) == 0:
            if "file" in request.FILES:
                uploaded_file = request.FILES["file"]
                file = File.objects.create(
                    file=uploaded_file,
                    sub_theme=sub_theme
                )

        return HttpResponseRedirect(reverse("theme_settings", args=[sub_theme.parent_theme.id,]))
    else:
        return HttpResponseRedirect(reverse("index"))


@login_required
def download_file(request, id):
    try:
        uploaded_file = File.objects.get(pk=id)
    except:
        return HttpResponseRedirect(reverse("index"))
    response = HttpResponse(FileWrapper(uploaded_file.file), content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=' + uploaded_file.file.name
    return response


@login_required
def delete_file(request, id):
    try:
        uploaded_file = File.objects.get(pk=id)
    except:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    uploaded_file.delete()
    if "subThemeId" in request.POST:
        try:
            sub_theme = SubTheme.objects.get(id=request.POST["subThemeId"])
        except:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect(reverse("theme_settings", args=[sub_theme.parent_theme.id,]))


@login_required
def cancel_theme(request, id):
    try:
        scheduled_theme = ScheduledTheme.objects.get(id=id)
    except:
        return HttpResponseRedirect(reverse("index"))
    scheduled_theme.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def edit_theme(request, id):
    try:
        theme = Theme.objects.get(id=id)
        journal = Journal.objects.get(id=theme.journal.id)
    except:
        return HttpResponseRedirect(reverse("index"))
    if "themeName" in request.POST:
        theme.name = request.POST["themeName"]
    if "description" in request.POST:
        theme.description = request.POST["description"]
    theme.save()
    return HttpResponseRedirect(reverse("journal_settings", args=[journal.id,]))


@login_required
def edit_sub_theme(request, id):
    try:
        sub_theme = SubTheme.objects.get(id=id)
        theme = Theme.objects.get(id=sub_theme.parent_theme.id)
    except:
        return HttpResponseRedirect(reverse("index"))
    if "subThemeName" in request.POST:
        sub_theme.name = request.POST["subThemeName"]
    if "description" in request.POST:
        sub_theme.description = request.POST["description"]
    sub_theme.save()
    return HttpResponseRedirect(reverse("theme_settings", args=[theme.id,]))


@login_required
def add_position(request):
    if "name" in request.POST:
        position = Position.objects.create(name=request.POST["name"])
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def delete_position(request, id):
    try:
        position = Position.objects.get(id=id)
    except:
        return HttpResponseRedirect(reverse("index"))
    user_list = UserProfile.objects.filter(position=position)
    for user in user_list:
        user.position = None
        user.save()
    position.delete()
    return HttpResponseRedirect(reverse("index"))

