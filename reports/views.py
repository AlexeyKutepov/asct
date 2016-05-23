from django.contrib.auth.decorators import login_required
from django.db.models import Max
from django.http import HttpResponseRedirect
from django.shortcuts import render
from main.models import ScheduledTheme, ScheduledSubTheme, ThemeExam, Company, Department, Journal
from exam.models import TestJournal
from authentication.models import UserProfile


class Counter:
    counter = 0

    def increment(self):
        self.counter += 1
        return self.counter

    def set_to_zero(self):
        self.counter = 0


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


def prepare_probationer_report(request, probationer_list, company_list):
    """
    Формирование отчёта "Ведомость сотрудника"
    :param request:
    :param probationer_list: список испытуемых для селектора
    :param company_list: список компаний для селектора
    :return:
    """
    try:
        user_data = UserProfile.objects.get(id=request.POST["probationer"])
        scheduled_theme_list = ScheduledTheme.objects.filter(user=user_data)
        scheduled_sub_theme_list = ScheduledSubTheme.objects.filter(user=user_data)
        journal_list = []
        for item in scheduled_theme_list:
            if item.theme.journal not in journal_list:
                journal_list.append(item.theme.journal)
        max_exam_list = ThemeExam.objects.filter(user=user_data).values('theme').annotate(
            result=Max('result')).order_by()
        exam_list = []
        for item in max_exam_list:
            exam_list.append(
                ThemeExam.objects.filter(user=user_data, theme=item['theme']).latest('result')
            )
    except:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    counter = Counter()
    return render(
        request,
        "reports/reports.html",
        {
            "probationer_list": probationer_list,
            "company_list": company_list,
            "user_data": user_data,
            "scheduled_theme_list": scheduled_theme_list,
            "scheduled_sub_theme_list": scheduled_sub_theme_list,
            "exam_list": exam_list,
            "journal_list": journal_list,
            "show_probationer_report": True,
            "counter": counter,
            "progress": calculate_progress(user_data)
        }
    )


def prepare_company_report(request, probationer_list, company_list):
    """
    Формирование отчёта "Мгновенный срез по компании"
    :param request:
    :param probationer_list: список испытуемых для селектора
    :param company_list: список компаний для селектора
    :return:
    """
    try:
        company = Company.objects.get(id=request.POST["company"])
        department_list = Department.objects.filter(company=company)
    except:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    company_report_data = []
    in_total_completed_probationer_count = 0
    in_total_probationer_count = 0
    in_total_theme_count = 0
    in_total_completed_theme_count = 0
    in_total_exam_count = 0
    in_total_completed_exam_count = 0
    in_total_assessment = 0
    for department in department_list:
        probationer_data_list = UserProfile.objects.filter(department=department, user_type=UserProfile.PROBATIONER, is_active=True)
        if len(probationer_data_list) == 0:
            continue
        else:
            in_total_probationer_count += len(probationer_data_list)
            completed_probationer_count = 0
            theme_count = 0
            completed_theme_count = 0
            exam_count = 0
            completed_exam_count = 0
            assessment = 0
            for probationer_data in probationer_data_list:
                theme_list = ScheduledTheme.objects.filter(user=probationer_data)
                completed_theme_list = ScheduledTheme.objects.filter(user=probationer_data,
                                                                     status=ScheduledTheme.COMPLETED)
                if len(theme_list) == len(completed_theme_list):
                    completed_probationer_count += 1
                    in_total_completed_probationer_count += 1
                theme_count += len(theme_list)
                in_total_theme_count += len(theme_list)
                completed_theme_count += len(completed_theme_list)
                in_total_completed_theme_count += len(completed_theme_list)

                exam_list = ThemeExam.objects.filter(user=probationer_data)
                exam_count += len(exam_list)
                in_total_exam_count += len(exam_list)
                for exam in exam_list:
                    if exam.result:
                        completed_exam_count += 1
                        in_total_completed_exam_count += 1
                        assessment += exam.result
                        in_total_assessment += exam.result

            result = {
                "department_name": department.name,
                "probationer_count": len(probationer_data_list),
                "completed_probationer_count": completed_probationer_count,
                "not_completed_probationer_count": len(probationer_data_list) - completed_probationer_count,
                "theme_progress": round(completed_theme_count / theme_count * 100, 1) if theme_count else 0,
                "exam_progress": round(completed_exam_count / exam_count * 100, 1) if completed_exam_count else 0,
                "assessment": assessment / completed_exam_count if completed_exam_count else 0,
            }
            company_report_data.append(result)
    in_total = {
        "probationer_count": in_total_probationer_count,
        "completed_probationer_count": in_total_completed_probationer_count,
        "not_completed_probationer_count": in_total_probationer_count - in_total_completed_probationer_count,
        "theme_progress": round(in_total_completed_theme_count / in_total_theme_count * 100, 1) if in_total_theme_count else 0,
        "exam_progress": round(in_total_completed_exam_count / in_total_exam_count * 100, 1) if in_total_completed_exam_count else 0,
        "assessment": in_total_assessment / in_total_completed_exam_count if in_total_completed_exam_count else 0,
    }

    return render(
        request,
        "reports/reports.html",
        {
            "probationer_list": probationer_list,
            "company_list": company_list,
            "company": company,
            "company_report_data": company_report_data,
            "in_total": in_total,
            "show_company_report": True,
        }
    )


def prepare_all_company_report(request, probationer_list, company_list):
    """
    Формирование отчёта "Мгновенный срез по группе компаний"
    :param request:
    :param probationer_list: список испытуемых для селектора
    :param company_list: список компаний для селектора
    :return:
    """
    all_company_report_data = []
    for company in company_list:
        try:
            department_list = Department.objects.filter(company=company)
        except:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        company_report_data = []
        in_total_completed_probationer_count = 0
        in_total_probationer_count = 0
        in_total_theme_count = 0
        in_total_completed_theme_count = 0
        in_total_exam_count = 0
        in_total_completed_exam_count = 0
        in_total_assessment = 0
        for department in department_list:
            probationer_data_list = UserProfile.objects.filter(department=department, user_type=UserProfile.PROBATIONER, is_active=True)
            if len(probationer_data_list) == 0:
                continue
            else:
                in_total_probationer_count += len(probationer_data_list)
                completed_probationer_count = 0
                theme_count = 0
                completed_theme_count = 0
                exam_count = 0
                completed_exam_count = 0
                assessment = 0
                for probationer_data in probationer_data_list:
                    theme_list = ScheduledTheme.objects.filter(user=probationer_data)
                    completed_theme_list = ScheduledTheme.objects.filter(user=probationer_data,
                                                                         status=ScheduledTheme.COMPLETED)
                    if len(theme_list) == len(completed_theme_list):
                        in_total_completed_probationer_count += 1
                        completed_probationer_count += 1
                    theme_count += len(theme_list)
                    in_total_theme_count += len(theme_list)
                    completed_theme_count += len(completed_theme_list)
                    in_total_completed_theme_count += len(completed_theme_list)

                    exam_list = ThemeExam.objects.filter(user=probationer_data)
                    exam_count += len(exam_list)
                    in_total_exam_count += len(exam_list)
                    for exam in exam_list:
                        if exam.result:
                            completed_exam_count += 1
                            in_total_completed_exam_count += 1
                            assessment += exam.result
                            in_total_assessment += exam.result

                result = {
                    "department_name": department.name,
                    "probationer_count": len(probationer_data_list),
                    "completed_probationer_count": completed_probationer_count,
                    "not_completed_probationer_count": len(probationer_data_list) - completed_probationer_count,
                    "theme_progress": round(completed_theme_count / theme_count * 100, 1) if theme_count else 0,
                    "exam_progress": round(completed_exam_count / exam_count * 100, 1) if completed_exam_count else 0,
                    "assessment": assessment / completed_exam_count if completed_exam_count else 0,
                }
                company_report_data.append(result)
        in_total = {
            "probationer_count": in_total_probationer_count,
            "completed_probationer_count": in_total_completed_probationer_count,
            "not_completed_probationer_count": in_total_probationer_count - in_total_completed_probationer_count,
            "theme_progress": round(in_total_completed_theme_count / in_total_theme_count * 100, 1) if in_total_theme_count else 0,
            "exam_progress": round(in_total_completed_exam_count / in_total_exam_count * 100, 1) if in_total_completed_exam_count else 0,
            "assessment": in_total_assessment / in_total_completed_exam_count if in_total_completed_exam_count else 0,
        }
        all_company_report_data.append(
            {
                "company": company,
                "report": company_report_data,
                "in_total": in_total
            }
        )

    return render(
        request,
        "reports/reports.html",
        {
            "probationer_list": probationer_list,
            "company_list": company_list,
            "all_company_report_data": all_company_report_data,
            "show_all_company_report": True,
        }
    )


def prepare_exam_list_report(request, probationer_list, company_list):
    """
    Формирование отчёта "Зачётный лист сотрудника"
    :param request:
    :param probationer_list: список испытуемых для селектора
    :param company_list: список компаний для селектора
    :return:
    """
    try:
        user_data = UserProfile.objects.get(id=request.POST["probationer"])
        journal_list = Journal.objects.filter(company=user_data.company)
        exam_list = ThemeExam.objects.filter(user=user_data)
    except:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    result_journal_list = []
    for journal in journal_list:
        isHasExam = False
        for exam in exam_list:
            if exam.theme.journal == journal:
                isHasExam = True
                break
        if isHasExam:
            result_journal_list.append(journal)
    if len(result_journal_list) == 0:
        result_journal_list = None
    return render(
        request,
        "reports/reports.html",
        {
            "probationer_list": probationer_list,
            "company_list": company_list,
            "user_data": user_data,
            "journal_list": result_journal_list,
            "exam_list": exam_list,
            "show_exam_list_report": True,
        }
    )


def prepare_test_report(request, probationer_list, company_list):
    """
    Формирование отчёта "План-график назначенных тестов"
    :param request:
    :param probationer_list: список испытуемых для селектора
    :param company_list: список компаний для селектора
    :return:
    """
    try:
        test_list = TestJournal.objects.all()
    except:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return render(
        request,
        "reports/reports.html",
        {
            "probationer_list": probationer_list,
            "company_list": company_list,
            "test_list": test_list,
            "show_test_report": True,
        }
    )


def prepare_department_report(request, probationer_list, company_list):
    """
    Формирование отчёта "Ведомость подразделения"
    :param request:
    :param probationer_list: список испытуемых для селектора
    :param company_list: список компаний для селектора
    :return:
    """
    try:
        department = Department.objects.get(id=request.POST["department"])
        user_list = UserProfile.objects.filter(department=department, user_type=UserProfile.PROBATIONER, is_active=True)
    except:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    result_list = []
    in_total_assessment = 0
    in_total_assessment_count = 0
    department_theme_progress = 0.0
    for user in user_list:
        exam_list = ThemeExam.objects.filter(user=user)
        assessment = 0
        assessment_count = 0
        for exam in exam_list:
            if exam.result:
                assessment += exam.result
                in_total_assessment += exam.result
                assessment_count += 1
                in_total_assessment_count += 1
        assessment = assessment/assessment_count if assessment_count != 0 else "Нет оценок по зачётам"

        theme_list = ScheduledTheme.objects.filter(user=user)
        completed_theme_list = ScheduledTheme.objects.filter(user=user,
                                                                    status=ScheduledTheme.COMPLETED)

        if len(theme_list) != 0 and len(theme_list) == len(completed_theme_list):
            progress = 100
            department_theme_progress += 1
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
            department_theme_progress += progress/100
        else:
            progress = "Темы не назначены"

        result_list.append(
            {
                "user": user,
                "progress": progress,
                "assessment": assessment if len(exam_list) != 0 else "Зачёты не назначены"
            }
        )
    in_total_assessment = in_total_assessment/in_total_assessment_count if in_total_assessment_count != 0 else 0


    return render(
        request,
        "reports/reports.html",
        {
            "probationer_list": probationer_list,
            "company_list": company_list,
            "department": department,
            "result_list": result_list,
            "in_total_progress": round((department_theme_progress)/len(user_list) * 100 if len(user_list) else 0, 2),
            "in_total_assessment": in_total_assessment,
            "show_department_report": True
        }
    )


@login_required
def reports(request):
    if request.user.user_type == UserProfile.PROBATIONER:
        result = {
            "status": "danger",
            "message": "Доступ запрещён"
        }
        return render(request, "alert.html", result)
    elif request.user.user_type == UserProfile.CURATOR:
        probationer_list = UserProfile.objects.filter(user_type=UserProfile.PROBATIONER, is_active=True).order_by("last_name")
        company_list = Company.objects.all().order_by("name")
    else:
        probationer_list = UserProfile.objects.filter(user_type=UserProfile.PROBATIONER, company=request.user.company, is_active=True)
        company_list = [request.user.company, ]
    if "probationer_report" in request.POST:
        return prepare_probationer_report(request, probationer_list, company_list)
    elif "department_report" in request.POST:
        return prepare_department_report(request, probationer_list, company_list)
    elif "company_report" in request.POST:
        return prepare_company_report(request, probationer_list, company_list)
    elif "all_company_report" in request.POST:
        return prepare_all_company_report(request, probationer_list, company_list)
    elif "exam_list_report" in request.POST:
        return prepare_exam_list_report(request, probationer_list, company_list)
    elif "test_report" in request.POST:
        return prepare_test_report(request, probationer_list, company_list)
    return render(
        request,
        "reports/reports.html",
        {
            "probationer_list": probationer_list,
            "company_list": company_list
        }
    )
