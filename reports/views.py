from django.contrib.auth.decorators import login_required
from django.db.models import Max
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from main.models import UserProfile, ScheduledTheme, ScheduledSubTheme, ThemeExam, Company, Department


class Counter:
    counter = 0

    def increment(self):
        self.counter += 1
        return self.counter

    def set_to_zero(self):
        self.counter = 0


def prepare_probationer_report(request, probationer_list, company_list):
    try:
        user_data = UserProfile.objects.get(id=request.POST["probationer"])
        scheduled_theme_list = ScheduledTheme.objects.filter(user=user_data)
        scheduled_sub_theme_list = ScheduledSubTheme.objects.filter(user=user_data)
        journal_list = []
        for item in scheduled_theme_list:
            if item.theme.journal not in journal_list:
                journal_list.append(item.theme.journal)
        max_exam_list = ThemeExam.objects.filter(user=user_data).values('theme').annotate(result=Max('result')).order_by()
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
            "counter": counter
        }
    )


def prepare_company_report(request, probationer_list, company_list):
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
        probationer_data_list = UserProfile.objects.filter(department=department, user_type=UserProfile.PROBATIONER)
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
                completed_theme_list = ScheduledTheme.objects.filter(user=probationer_data, status=ScheduledTheme.COMPLETED)
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
                "theme_progress": completed_theme_count/theme_count * 100 if theme_count else 0,
                "exam_progress": completed_exam_count/exam_count * 100 if completed_exam_count else 0,
                "assessment": assessment/completed_exam_count if completed_exam_count else 0,
            }
            company_report_data.append(result)
    in_total = {
         "probationer_count": in_total_probationer_count,
         "completed_probationer_count": in_total_completed_probationer_count,
         "not_completed_probationer_count": in_total_probationer_count - in_total_completed_probationer_count,
         "theme_progress": in_total_completed_theme_count/in_total_theme_count * 100 if in_total_theme_count else 0,
         "exam_progress": in_total_completed_exam_count/in_total_exam_count * 100 if in_total_completed_exam_count else 0,
         "assessment": in_total_assessment/in_total_completed_exam_count if in_total_completed_exam_count else 0,
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
            probationer_data_list = UserProfile.objects.filter(department=department, user_type=UserProfile.PROBATIONER)
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
                    completed_theme_list = ScheduledTheme.objects.filter(user=probationer_data, status=ScheduledTheme.COMPLETED)
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
                    "theme_progress": completed_theme_count/theme_count * 100 if theme_count else 0,
                    "exam_progress": completed_exam_count/exam_count * 100 if completed_exam_count else 0,
                    "assessment": assessment/completed_exam_count if completed_exam_count else 0,
                }
                company_report_data.append(result)
        in_total = {
             "probationer_count": in_total_probationer_count,
             "completed_probationer_count": in_total_completed_probationer_count,
             "not_completed_probationer_count": in_total_probationer_count - in_total_completed_probationer_count,
             "theme_progress": in_total_completed_theme_count/in_total_theme_count * 100 if in_total_theme_count else 0,
             "exam_progress": in_total_completed_exam_count/in_total_exam_count * 100 if in_total_completed_exam_count else 0,
             "assessment": in_total_assessment/in_total_completed_exam_count if in_total_completed_exam_count else 0,
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


@login_required
def reports(request):
    if request.user.user_type == UserProfile.PROBATIONER:
       result = {
           "status": "danger",
           "message": "Доступ запрещён"
           }
       return render(request, "alert.html", result)
    elif request.user.user_type == UserProfile.CURATOR:
        probationer_list = UserProfile.objects.filter(user_type=UserProfile.PROBATIONER)
        company_list = Company.objects.all()
    else:
        probationer_list = UserProfile.objects.filter(user_type=UserProfile.PROBATIONER, company=request.user.company)
        company_list = [request.user.company,]
    if "probationer_report" in request.POST:
        return prepare_probationer_report(request, probationer_list, company_list)
    elif "company_report" in request.POST:
        return prepare_company_report(request, probationer_list, company_list)
    elif "all_company_report" in request.POST:
        return prepare_all_company_report(request, probationer_list, company_list)
    return render(
        request,
        "reports/reports.html",
        {
            "probationer_list": probationer_list,
            "company_list": company_list
        }
    )
