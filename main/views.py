import datetime
from django.utils import timezone
from mimetypes import MimeTypes
from wsgiref.util import FileWrapper
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from asct import settings
from authentication.models import UserProfile
from main.models import Company, Department, Journal, Theme, SubTheme, ScheduledTheme, ScheduledSubTheme, \
    File, Position, ThemeExam
from exam.models import Test, TestJournal


def test_page(request):
    return render(request, "test_page.html")


def calculate_progress(user):
    theme_list = ScheduledTheme.objects.filter(user=user)
    completed_theme_list = ScheduledTheme.objects.filter(user=user,
                                                                status=ScheduledTheme.COMPLETED)

    if len(theme_list) != 0 and len(theme_list) == len(completed_theme_list):
        progress = 100
    elif len(theme_list) != 0:
        theme_progress = len(completed_theme_list)
        sub_theme_progress = 0.0
        for theme in theme_list:
            if theme.status != ScheduledTheme.COMPLETED:
                sub_theme_list = ScheduledSubTheme.objects.filter(scheduled_theme=theme)
                if len(sub_theme_list) != 0:
                    completed_sub_theme_list = ScheduledSubTheme.objects.filter(scheduled_theme=theme, status=ScheduledSubTheme.COMPLETED)
                    sub_theme_progress += round(len(completed_sub_theme_list) / len(sub_theme_list) if len(sub_theme_list) else 0, 2)
        progress = round((theme_progress + sub_theme_progress)/len(theme_list)*100 if len(theme_list) else 0, 2)
    else:
        progress = None
    return progress


def prepare_curator_page(request):
    user_list = UserProfile.objects.filter(is_active=True).order_by('last_name')
    fire_user_list = UserProfile.objects.filter(is_active=False).order_by('last_name')
    company_list = Company.objects.all().order_by('name')
    position_list = Position.objects.all().order_by('name')
    return render(
        request,
        "main/curator_profile.html",
        {
            "user_list": user_list,
            "company_list": company_list,
            "position_list": position_list,
            "fire_user_list": fire_user_list
        }
    )


def prepare_admin_page(request):
    user_list = UserProfile.objects.filter(
        Q(user_type=UserProfile.OPERATOR, company=request.user.company, is_active=True) | Q(user_type=UserProfile.PROBATIONER,
                                                                            company=request.user.company, is_active=True)
    ).order_by('last_name')
    fire_user_list = UserProfile.objects.filter(
        Q(user_type=UserProfile.OPERATOR, company=request.user.company, is_active=True) | Q(user_type=UserProfile.PROBATIONER,
                                                                            company=request.user.company, is_active=False)
    ).order_by('last_name')
    position_list = Position.objects.all().order_by('name')
    return render(
        request,
        "main/admin_profile.html",
        {
            "user_list": user_list,
            "position_list": position_list,
            "fire_user_list": fire_user_list
        }
    )


def prepare_operator_page(request):
    probationer_list = UserProfile.objects.filter(user_type=UserProfile.PROBATIONER, company=request.user.company, is_active=True).order_by('last_name')
    fire_user_list = UserProfile.objects.filter(user_type=UserProfile.PROBATIONER, company=request.user.company, is_active=False).order_by('last_name')
    return render(
        request,
        "main/operator_profile.html",
        {
            "probationer_list": probationer_list,
            "fire_user_list": fire_user_list
        }
    )


def prepare_probationer_page(request):
    scheduled_theme_list = ScheduledTheme.objects.filter(user=request.user)
    for scheduled_theme in scheduled_theme_list:
        if scheduled_theme.date_to < timezone.now() - timezone.timedelta(days=1) and scheduled_theme.status != ScheduledTheme.COMPLETED and scheduled_theme.status != ScheduledTheme.OVERDUE:
            scheduled_theme.status = ScheduledTheme.OVERDUE
            scheduled_theme.save()
    exam_list = ThemeExam.objects.filter(user=request.user)
    test_list = TestJournal.objects.filter(user=request.user)
    for test in test_list:
        if test.date_to < timezone.now() - timezone.timedelta(days=1) and test.status != TestJournal.COMPLETED and test.status != TestJournal.OVERDUE:
            test.status = TestJournal.OVERDUE
            test.save()

    return render(
        request,
        "main/probationer_profile.html",
        {
            "scheduled_theme_list": scheduled_theme_list,
            "exam_list": exam_list,
            "test_list": test_list,
            "progress": calculate_progress(request.user)
        }
    )


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
def get_position_list(request):
    if "id" in request.POST:
        department = Department.objects.get(id=request.POST["id"])
        result = {}
        list = []
        for position in department.position.all():
            list.append({
                "id": position.id,
                "name": position.name
            })
        result["position_list"] = list
        return JsonResponse(result)
    else:
        return JsonResponse({"position_list": []})


@login_required
def get_user_list_by_department(request):
    if "id" in request.POST:
        department = Department.objects.get(id=request.POST["id"])
        user_list = UserProfile.objects.filter(department=department, is_active=True)
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
    if "userId" in request.POST:
        try:
            user = UserProfile.objects.get(id=request.POST["userId"])
        except:
            user = None
        if user and request.user.user_type != UserProfile.PROBATIONER:
            journal_list = Journal.objects.filter(
                Q(company=user.company) & (Q(department=user.department) | Q(department=None)))
        else:
            journal_list = []
    elif request.user.user_type == UserProfile.CURATOR:
        journal_list = Journal.objects.all()
    elif request.user.user_type != UserProfile.PROBATIONER:
        journal_list = Journal.objects.filter(company=request.user.company)
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
def add_department(request):
    try:
        company = Company.objects.get(id=request.POST["companyId"])
    except:
        result = {
            "status": "danger",
            "message": "Ошибка выполнения операции!"
        }
        return render(request, "alert.html", result)
    if "name" in request.POST:
        department_list_in_base = Department.objects.filter(company=company, name=request.POST["name"])
        if len(department_list_in_base) == 0:
            Department.objects.create(name=request.POST["name"], company=company)
        else:
            result = {
                "status": "danger",
                "message": "Ошибка выполнения операции! Подразделение " + request.POST[
                    "name"] + " уже существует в компании " + company.name
            }
            return render(request, "alert.html", result)

    return HttpResponseRedirect(reverse("edit_company", args=[company.id, ]))


@login_required
def department_settings(request, id):
    department = Department.objects.get(id=id)
    position_list = Position.objects.all().order_by('name')
    if "save" in request.POST:
        department.name = request.POST["department"]
        in_department_list = request.POST.getlist("inDepartment")
        i = 0
        for position in position_list:
            if str(i) in in_department_list:
                if not position in department.position.all():
                    department.position.add(position)
            else:
                if position in department.position.all():
                    department.position.remove(position)
            i += 1
        department.save()
        result = {
            "status": "success",
            "message": "Изменения успешно сохранены!"
        }
        return render(request, "alert.html", result)
    else:
        return render(
            request,
            "main/department_settings.html",
            {
                "department": department,
                "position_list": position_list,
                "department_position_list": department.position.all()
            }
        )


@login_required
def delete_department(request, id):
    department = Department.objects.get(id=id)
    company = department.company
    # ВАЖНЫЙ МОМЕНТ: перед удалением департамента нужно почистить юзеров от него, иначе они будут удалены
    user_list = UserProfile.objects.filter(department=department)
    for item in user_list:
        item.department = None
        item.save()
    department.delete()

    return HttpResponseRedirect(reverse("edit_company", args=[company.id, ]))


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
        if "bindDepartment" in request.POST and request.POST["bindDepartment"] == 'on' and "department" in request.POST:
            department = Department.objects.get(id=request.POST["department"])
        else:
            department = None
        journal = Journal.objects.create(
            name=request.POST["name"],
            description=request.POST["description"],
            owner=request.user,
            company=company,
            department=department
        )
        return HttpResponseRedirect(reverse("journal_settings", args=[journal.id, ]))
    else:
        if request.user.user_type == UserProfile.CURATOR:
            company_list = Company.objects.all()
        else:
            company_list = []
        if request.user.company.id:
            company = Company.objects.get(id=request.user.company.id)
            department_list = Department.objects.filter(company=company)
        else:
            department_list = []
        return render(
            request,
            "main/create_journal.html",
            {
                "company_list": company_list,
                "department_list": department_list
            }
        )


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
    if "bindDepartment" in request.POST and request.POST["bindDepartment"] == 'on' and "department" in request.POST:
        journal.department = Department.objects.get(id=request.POST["department"])
    else:
        journal.department = None
    journal.save()
    return HttpResponseRedirect(reverse("journal_settings", args=[journal.id, ]))


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
    test_list = Test.objects.filter(journal=journal)
    for test in test_list:
        cloned_test = Test.objects.create(
            name=test.name,
            description=test.description,
            test=test.test,
            journal=cloned_journal,
            author=test.author,
            date_and_time=timezone.now()
        )
    result = {
        "status": "success",
        "message": "Программа \"" + journal.name + "\" дублирована для компании \"" + company.name + "\""
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
    test_list = Test.objects.filter(journal=journal)
    if request.user.user_type == UserProfile.CURATOR:
        company_list = Company.objects.all()
    else:
        company_list = []
    department_list = Department.objects.filter(company=journal.company)
    return render(
        request,
        "main/journal_settings.html",
        {
            "journal": journal,
            "theme_list": theme_list,
            "company_list": company_list,
            "test_list": test_list,
            "department_list": department_list
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
        return HttpResponseRedirect(reverse("journal_settings", args=[journal.id, ]))
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
    return HttpResponseRedirect(reverse("journal_settings", args=[journal.id, ]))


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
    if theme:
        examiner_list = UserProfile.objects.filter(~Q(user_type=UserProfile.PROBATIONER), company=theme.journal.company, is_active=True)
    else:
        examiner_list = UserProfile.objects.filter(~Q(user_type=UserProfile.PROBATIONER), is_active=True)
    sub_theme_list = SubTheme.objects.filter(parent_theme=theme)
    if request.user.user_type == UserProfile.CURATOR:
        scheduled_theme_list = ScheduledTheme.objects.filter(theme=theme)
    else:
        user_list = UserProfile.objects.filter(company=request.user.company, is_active=True)
        scheduled_theme_list = ScheduledTheme.objects.filter(theme=theme, user__in=user_list)
    for scheduled_theme in scheduled_theme_list:
        if scheduled_theme.date_to < timezone.now() - timezone.timedelta(days=1) and scheduled_theme.status != ScheduledTheme.COMPLETED and scheduled_theme.status != ScheduledTheme.OVERDUE:
            scheduled_theme.status = ScheduledTheme.OVERDUE
            scheduled_theme.save()
    exam_list = ThemeExam.objects.filter(theme=theme)
    return render(
        request,
        "main/theme_settings.html",
        {
            "theme": theme,
            "sub_theme_list": sub_theme_list,
            "scheduled_theme_list": scheduled_theme_list,
            "exam_list": exam_list,
            "examiner_list": examiner_list
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
        return HttpResponseRedirect(reverse("theme_settings", args=[theme.id, ]))
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
    return HttpResponseRedirect(reverse("theme_settings", args=[theme.id, ]))


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
            date_to=datetime.datetime.strptime(request.POST["dateTo"], "%d.%m.%Y"),
            user=user,
            theme=theme
        )
        sub_theme_list = SubTheme.objects.filter(parent_theme=theme)
        for item in sub_theme_list:
            ScheduledSubTheme.objects.create(
                date_to=datetime.datetime.strptime(request.POST["dateTo"], "%d.%m.%Y"),
                user=user,
                sub_theme=item,
                scheduled_theme=scheduled_theme
            )
        try:
            send_mail(
                'Вам назначена тема в ASCT',
                'Здравствуйте ' + user.first_name + '! \n \n Вам назначена тема для изучения: \"' + theme.name
                + '\" \n\n Срок до ' + request.POST["dateTo"]
                + ' \n\n Для изучения перейдите по ссылке: ' + request.build_absolute_uri(
                    reverse("probationer_theme_settings", args=[scheduled_theme.id, ])),
                getattr(settings, "EMAIL_HOST_USER", None),
                [user.email],
                fail_silently=False
            )
        except:
            pass
        return HttpResponseRedirect(reverse("theme_settings", args=[theme.id, ]))
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
            date_to=datetime.datetime.strptime(request.POST["dateTo"], "%d.%m.%Y"),
            user=user,
            theme=theme
        )
        sub_theme_list = SubTheme.objects.filter(parent_theme=theme)
        for item in sub_theme_list:
            ScheduledSubTheme.objects.create(
                date_to=datetime.datetime.strptime(request.POST["dateTo"], "%d.%m.%Y"),
                user=user,
                sub_theme=item,
                scheduled_theme=scheduled_theme
            )
        try:
            send_mail(
                'Вам назначена тема в ASCT',
                'Здравствуйте ' + user.first_name + '! \n \n Вам назначена тема для изучения: \"' + theme.name
                + '\" \n\n Срок до ' + request.POST["dateTo"]
                + ' \n\n Для изучения перейдите по ссылке: ' + request.build_absolute_uri(
                    reverse("probationer_theme_settings", args=[scheduled_theme.id, ])),
                getattr(settings, "EMAIL_HOST_USER", None),
                [user.email],
                fail_silently=False
            )
        except:
            pass
        return HttpResponseRedirect(reverse("user_info", args=[user.id, ]))
    else:
        return HttpResponseRedirect(reverse("index"))


@login_required
def cancel_theme(request, id):
    try:
        scheduled_theme = ScheduledTheme.objects.get(id=id)
    except:
        return HttpResponseRedirect(reverse("index"))
    scheduled_theme.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def edit_scheduled_theme(request, id):
    try:
        scheduled_theme = ScheduledTheme.objects.get(id=id)
    except:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    if "dateTo" in request.POST:
        scheduled_theme.date_to = datetime.datetime.strptime(request.POST["dateTo"], "%d.%m.%Y")
        if scheduled_theme.status == ScheduledTheme.OVERDUE:
            scheduled_theme.status = ScheduledTheme.ASSIGNED
        scheduled_theme.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


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
            datetime=datetime.datetime.strptime(request.POST["datetime"], "%d.%m.%Y %H:%M"),
            place=request.POST["place"],
        )
        try:
            send_mail(
                'Вам назначен зачёт в ASCT',
                'Здравствуйте ' + user.first_name + '! \n \n Вам назначен зачёт по теме: \"' + theme.name
                + '\" \n\n Дата и время проведения зачёта: ' + str(theme_exam.datetime).replace('T', ' ')
                + ' \n\n Место проведения зачёта: ' + request.POST["place"]
                + ' \n\n Экзаменатор: ' + examiner.get_full_name()
                ,
                getattr(settings, "EMAIL_HOST_USER", None),
                [user.email],
                fail_silently=False
            )
        except:
            pass
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def edit_exam(request, id):
    if request.user.user_type == UserProfile.PROBATIONER:
        result = {
            "status": "danger",
            "message": "Доступ запрещён"
        }
        return render(request, "alert.html", result)
    if "save" in request.POST:
        try:
            theme_exam = ThemeExam.objects.get(id=id)
            user = UserProfile.objects.get(id=request.POST["user"])
            examiner = UserProfile.objects.get(id=request.POST["examiner"])
        except:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        theme_exam.examiner = examiner
        theme_exam.datetime = datetime.datetime.strptime(request.POST["datetime"], "%d.%m.%Y %H:%M")
        theme_exam.place = request.POST["place"]
        theme_exam.save()
        try:
            send_mail(
                'Изменение информации по зачёту в ASCT',
                'Здравствуйте ' + user.first_name + '! \n \n Информация по зачёту была изменена. Актуальная информация:  \n \n Зачёт по теме: \"' + theme_exam.theme.name
                + '\" \n\n Дата и время проведения зачёта: ' + str(theme_exam.datetime).replace('T', ' ')
                + ' \n\n Место проведения зачёта: ' + request.POST["place"]
                + ' \n\n Экзаменатор: ' + examiner.get_full_name()
                ,
                getattr(settings, "EMAIL_HOST_USER", None),
                [user.email],
                fail_silently=False
            )
        except:
            pass
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def get_probationer_list(request):
    if request.user.user_type != UserProfile.PROBATIONER and "themeId" in request.POST:
        try:
            theme = Theme.objects.get(id=request.POST["themeId"])
        except:
            theme = None
        if theme:
            if theme.journal.department:
                probationer_list = UserProfile.objects.filter(
                    Q(user_type=UserProfile.PROBATIONER)
                    & Q(company=theme.journal.company)
                    & Q(department=theme.journal.department)
                    & Q(is_active=True)
                )
            else:
                probationer_list = UserProfile.objects.filter(
                    user_type=UserProfile.PROBATIONER,
                    company=theme.journal.company,
                    is_active=True
                )
        else:
            probationer_list = UserProfile.objects.filter(user_type=UserProfile.PROBATIONER, is_active=True)
        result = {}
        list = []
        for item in probationer_list:
            list.append({
                "id": item.id,
                "name": item.get_full_name()
            })
        result["probationer_list"] = list
        return JsonResponse(result)
    elif request.user.user_type != UserProfile.PROBATIONER and "testId" in request.POST:
        try:
            test = Test.objects.get(id=request.POST["testId"])
        except:
            test = None
        if test:
            if test.journal.department:
                probationer_list = UserProfile.objects.filter(
                    Q(user_type=UserProfile.PROBATIONER)
                    & Q(company=test.journal.company)
                    & Q(department=test.journal.department)
                    & Q(is_active=True)
                )
            else:
                probationer_list = UserProfile.objects.filter(
                    user_type=UserProfile.PROBATIONER,
                    company=test.journal.company,
                    is_active=True
                )
        else:
            probationer_list = UserProfile.objects.filter(user_type=UserProfile.PROBATIONER, is_active=True)
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
            examiner_list = UserProfile.objects.filter(~Q(user_type=UserProfile.PROBATIONER),
                                                       company=theme.journal.company, is_active=True)
        else:
            examiner_list = UserProfile.objects.filter(~Q(user_type=UserProfile.PROBATIONER), is_active=True)
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
    examiner_list = UserProfile.objects.filter(~Q(user_type=UserProfile.PROBATIONER), company=user_data.company, is_active=True)
    scheduled_theme_list = ScheduledTheme.objects.filter(user=user_data)
    for scheduled_theme in scheduled_theme_list:
        if scheduled_theme.date_to < timezone.now() - timezone.timedelta(days=1) and scheduled_theme.status != ScheduledTheme.COMPLETED and scheduled_theme.status != ScheduledTheme.OVERDUE:
            scheduled_theme.status = ScheduledTheme.OVERDUE
            scheduled_theme.save()
    exam_list = ThemeExam.objects.filter(user=user_data)
    test_list = TestJournal.objects.filter(user=user_data)
    for test in test_list:
        if test.date_to < timezone.now() - timezone.timedelta(days=1) and test.status != TestJournal.COMPLETED and test.status != TestJournal.OVERDUE:
            test.status = TestJournal.OVERDUE
            test.save()
    assessment = None
    assessment_count = 0
    for exam in exam_list:
        if exam.result:
            if not assessment:
                assessment = 0
            assessment += exam.result
            assessment_count += 1
    if not assessment or assessment_count == 0:
        assessment = None
    else:
        assessment = round(assessment / assessment_count, 2)

    return render(
        request,
        "main/user_info.html",
        {
            "user_data": user_data,
            "scheduled_theme_list": scheduled_theme_list,
            "exam_list": exam_list,
            "test_list": test_list,
            "examiner_list": examiner_list,
            "assessment": assessment,
            "progress": calculate_progress(user_data)
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
def get_test_list_by_journal(request):
    if "id" in request.POST:
        journal = Journal.objects.get(id=request.POST["id"])
        test_list = Test.objects.filter(journal=journal)
        result = {}
        list = []
        for item in test_list:
            list.append({
                "id": item.id,
                "name": item.name,
            })
        result["test_list"] = list
        return JsonResponse(result)
    else:
        return JsonResponse({"test_list": []})


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
        "message": "Программа " + name + " успешно удалёна!"
    }
    return render(request, "alert.html", result)


@login_required
def probationer_theme_settings(request, id):
    try:
        scheduled_theme = ScheduledTheme.objects.get(id=id)
    except:
        return HttpResponseRedirect(reverse("index"))
    if scheduled_theme.date_to < timezone.now() - timezone.timedelta(days=1) and scheduled_theme.status != ScheduledTheme.COMPLETED and scheduled_theme.status != ScheduledTheme.OVERDUE:
        scheduled_theme.status = ScheduledTheme.OVERDUE
        scheduled_theme.save()
    sub_theme_list = SubTheme.objects.filter(parent_theme=scheduled_theme.theme)
    scheduled_sub_theme_list = ScheduledSubTheme.objects.filter(sub_theme__in=sub_theme_list, user=request.user,
                                                                scheduled_theme=scheduled_theme)
    return render(
        request,
        "main/probationer_theme_settings.html",
        {
            "scheduled_theme": scheduled_theme,
            "scheduled_sub_theme_list": scheduled_sub_theme_list,
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
    return HttpResponseRedirect(reverse("probationer_theme_settings", args=[id, ]))


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
    return HttpResponseRedirect(reverse("probationer_theme_settings", args=[id, ]))


@login_required
def sub_theme_in_work(request, id):
    try:
        scheduled_sub_theme = ScheduledSubTheme.objects.get(id=id)
    except:
        return HttpResponseRedirect(reverse("index"))
    scheduled_sub_theme.status = ScheduledSubTheme.IN_WORK
    scheduled_sub_theme.save()
    return HttpResponseRedirect(reverse("probationer_theme_settings", args=[scheduled_sub_theme.scheduled_theme.id, ]))


@login_required
def sub_theme_completed(request, id):
    try:
        scheduled_sub_theme = ScheduledSubTheme.objects.get(id=id)
    except:
        return HttpResponseRedirect(reverse("index"))
    scheduled_sub_theme.status = ScheduledSubTheme.COMPLETED
    scheduled_sub_theme.save()

    scheduled_sub_theme_list = ScheduledSubTheme.objects.filter(scheduled_theme=scheduled_sub_theme.scheduled_theme)
    scheduled_sub_theme_list_completed = ScheduledSubTheme.objects.filter(
        scheduled_theme=scheduled_sub_theme.scheduled_theme, status=ScheduledSubTheme.COMPLETED)
    scheduled_sub_theme.scheduled_theme.progress = int(
        (100 / len(scheduled_sub_theme_list)) * len(scheduled_sub_theme_list_completed))
    if scheduled_sub_theme.scheduled_theme.progress == 100:
        scheduled_sub_theme.scheduled_theme.status = ScheduledTheme.COMPLETED
    scheduled_sub_theme.scheduled_theme.save()

    return HttpResponseRedirect(reverse("probationer_theme_settings", args=[scheduled_sub_theme.scheduled_theme.id, ]))


@login_required
def upload_file_to_sub_theme(request):
    if "subThemeId" in request.POST:
        try:
            sub_theme = SubTheme.objects.get(id=request.POST["subThemeId"])
        except:
            return HttpResponseRedirect(reverse("index"))
        if "file" in request.FILES:
            uploaded_file = request.FILES["file"]
            file = File.objects.create(
                file=uploaded_file,
                sub_theme=sub_theme
            )
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def manage_files(request, id):
    try:
        sub_theme = SubTheme.objects.get(id=id)
        file_list = File.objects.filter(sub_theme=sub_theme)
    except:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return render(
        request,
        "main/manage_files.html",
        {
            "sub_theme": sub_theme,
            "file_list": file_list
        }
    )


@login_required
def download_file(request, id):
    try:
        uploaded_file = File.objects.get(pk=id)
    except:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    mime = MimeTypes()
    mime_type = mime.guess_type(uploaded_file.file.file.name)
    response = HttpResponse(FileWrapper(uploaded_file.file), content_type=mime_type[0])
    response['Content-Disposition'] = 'attachment; filename=' + uploaded_file.file.name
    return response


@login_required
def delete_file(request, id):
    try:
        uploaded_file = File.objects.get(pk=id)
    except:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    uploaded_file.delete()
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
    return HttpResponseRedirect(reverse("journal_settings", args=[journal.id, ]))


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
    return HttpResponseRedirect(reverse("theme_settings", args=[theme.id, ]))


@login_required
def add_position(request):
    if "name" in request.POST:
        position = Position.objects.create(name=request.POST["name"])
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def edit_position(request, id):
    try:
        position = Position.objects.get(id=id)
    except:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    if "name" in request.POST:
        position.name = request.POST["name"]
        position.save()
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


@login_required
def set_result(request, id):
    try:
        exam = ThemeExam.objects.get(id=id)
    except:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    exam.result = request.POST["result"]
    exam.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def cancel_exam(request, id):
    try:
        exam = ThemeExam.objects.get(id=id)
    except:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    exam.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
