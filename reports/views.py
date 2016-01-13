from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from main.models import UserProfile, ScheduledTheme, ScheduledSubTheme, ThemeExam, Company


class Counter:
    counter = 0

    def increment(self):
        self.counter += 1
        return self.counter

    def set_to_zero(self):
        self.counter = 0


def prepare_probationer_report(request, probationer_list):
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
            "user_data": user_data,
            "scheduled_theme_list": scheduled_theme_list,
            "scheduled_sub_theme_list": scheduled_sub_theme_list,
            "exam_list": exam_list,
            "journal_list": journal_list,
            "show_probationer_report": True,
            "counter": counter
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
        return prepare_probationer_report(request, probationer_list)
    return render(
        request,
        "reports/reports.html",
        {
            "probationer_list": probationer_list,
            "company_list": company_list
        }
    )
