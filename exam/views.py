import datetime
import pickle

from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.exceptions import SuspiciousOperation
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from asct import settings
from exam.asct_test.asct_test import AsctTest, TestType, Question, CloseAnswer, Answer, AsctResult
from authentication.models import UserProfile
from exam.models import Journal, Test, TestImage, TestJournal, Progress


TYPE_LIST = [
    "Содержит один или несколько правильных вариантов ответа",
    "Содержит только один правильный вариант ответа",
    "Вопрос со свободной формой ответа",
]


@login_required
def create_new_test(request):
    """
    Создание нового теста
    :param request:
    :return:
    """
    if request.user.user_type == UserProfile.PROBATIONER:
        result = {
            "status": "danger",
            "message": "Доступ запрещён"
        }
        return render(request, "alert.html", result)
    if "save" and "name" and "description" in request.POST:
        try:
            journal = Journal.objects.get(id=request.POST["save"])
        except:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        test = Test.objects.create(
            name=request.POST["name"],
            description=request.POST["description"],
            journal=journal,
            author=request.user,
        )
        return HttpResponseRedirect(reverse("create_new_question", args=[test.id]))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def create_new_question(request, id):
    """
    Создание нового вопроса для теста
    :param request:
    :param id: id of the test
    :return:
    """
    if request.user.user_type == UserProfile.PROBATIONER:
        result = {
            "status": "danger",
            "message": "Доступ запрещён"
        }
        return render(request, "alert.html", result)
    test = Test.objects.get(id=id)
    if request.user != test.author:
        raise SuspiciousOperation("Некорректный id теста")
    if "type" in request.POST and int(request.POST["type"]) in (1, 2, 3):
        if test.test is None or test.test == b'':
            exam_test = AsctTest()
        else:
            exam_test = pickle.loads(test.test)
        question_type = TestType(int(request.POST["type"]))

        if "question" in request.POST:
            question = Question(request.POST["question"], question_type)
        else:
            question = Question(None, question_type)

        if "image" in request.FILES:
            image = TestImage.objects.get_or_create(image=request.FILES["image"])
            image_id = image[0].id
        else:
            image_id = None
        question.set_image(image_id)

        if question_type is TestType.CLOSE_TYPE_SEVERAL_CORRECT_ANSWERS:
            i = 1
            while "answer" + str(i) in request.POST:
                question.add_new_answer(
                    CloseAnswer(
                        answer=request.POST["answer" + str(i)],
                        is_correct=str(i) in request.POST.getlist("trueAnswer")
                    )
                )
                i += 1
        elif question_type is TestType.CLOSE_TYPE_ONE_CORRECT_ANSWER:
            i = 1
            while "answer" + str(i) in request.POST:
                question.add_new_answer(
                    CloseAnswer(
                        answer=request.POST["answer" + str(i)],
                        is_correct=str(i) == request.POST["trueAnswer"]
                    )
                )
                i += 1
        elif question_type is TestType.OPEN_TYPE:
            question.add_new_answer(
                Answer(
                    request.POST["openAnswer"],
                    "checkManually" in request.POST
                )
            )

        exam_test.add_question(question)
        test.test = pickle.dumps(exam_test)
        test.save()
        if "complete" in request.POST:
            return HttpResponseRedirect(reverse("journal_settings", args=[test.journal.id, ]))
        else:
            return render(
                request,
                "test/create_question.html",
                {
                    "number_of_question": len(exam_test.get_questions()) + 1,
                    "type_list": TYPE_LIST,
                    "test_id": id
                }
            )
    else:
        return render(
            request,
            "test/create_question.html",
            {
                "type_list": TYPE_LIST,
                "test_id": id
            }
        )


@login_required(login_url='/')
def edit_test(request, id):
    """
    Edits the test
    :param request:
    :param id: id of test
    :return:
    """
    if request.user.user_type == UserProfile.PROBATIONER:
        result = {
            "status": "danger",
            "message": "Доступ запрещён"
        }
        return render(request, "alert.html", result)
    id = int(id)
    test = Test.objects.get(id=id)

    if "save" in request.POST:
        test.name = request.POST["name"]
        test.description = request.POST["description"]
        test.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    if test.test:
        exam_test = pickle.loads(test.test)
        question_list = exam_test.get_questions()
    else:
        question_list = None

    return render(
        request,
        "test/edit_test.html",
        {
            "test": test,
            "question_list": question_list
        }
    )


@login_required
def delete_test(request, id):
    if request.user.user_type == UserProfile.PROBATIONER:
        result = {
            "status": "danger",
            "message": "Доступ запрещён"
        }
        return render(request, "alert.html", result)
    try:
        Test.objects.get(id=id).delete()
    except:
        pass
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def add_question(request, id):
    """
    Adds the question to test
    :param request:
    :param id: id of the test
    :return:
    """
    if request.user.user_type == UserProfile.PROBATIONER:
        result = {
            "status": "danger",
            "message": "Доступ запрещён"
        }
        return render(request, "alert.html", result)
    test = Test.objects.get(id=id)
    if test.test is None or test.test == b'':
        asct_test = AsctTest()
    else:
        asct_test = pickle.loads(test.test)

    if request.user != test.author:
        raise SuspiciousOperation("Некорректный id теста")
    if "type" in request.POST and int(request.POST["type"]) in (1, 2, 3):
        question_type = TestType(int(request.POST["type"]))

        if "question" in request.POST:
            question = Question(request.POST["question"], question_type)
        else:
            question = Question(None, question_type)

        if "image" in request.FILES:
            image = TestImage.objects.get_or_create(image=request.FILES["image"])
            image_id = image[0].id
        else:
            image_id = None
        question.set_image(image_id)

        if question_type is TestType.CLOSE_TYPE_SEVERAL_CORRECT_ANSWERS:
            i = 1
            while "answer" + str(i) in request.POST:
                question.add_new_answer(
                    CloseAnswer(
                        answer=request.POST["answer" + str(i)],
                        is_correct=str(i) in request.POST.getlist("trueAnswer")
                    )
                )
                i += 1
        elif question_type is TestType.CLOSE_TYPE_ONE_CORRECT_ANSWER:
            i = 1
            while "answer" + str(i) in request.POST:
                question.add_new_answer(
                    CloseAnswer(
                        answer=request.POST["answer" + str(i)],
                        is_correct=str(i) == request.POST["trueAnswer"]
                    )
                )
                i += 1
        elif question_type is TestType.OPEN_TYPE:
            question.add_new_answer(
                Answer(
                    request.POST["openAnswer"],
                    "checkManually" in request.POST
                )
            )

        asct_test.add_question(question)
        test.test = pickle.dumps(asct_test)
        test.save()

        return HttpResponseRedirect(reverse("edit_test", args=[id]))
    else:
        return render(
            request,
            "test/add_question.html",
            {
                "number_of_question": len(asct_test.get_questions()) + 1,
                "type_list": TYPE_LIST,
                "test_id": id
            }
        )


@login_required
def edit_question(request, id, number):
    """
    Edits the question in the test
    :param request:
    :param id: id of test
    :param number: number of question
    :return:
    """
    if request.user.user_type == UserProfile.PROBATIONER:
        result = {
            "status": "danger",
            "message": "Доступ запрещён"
        }
        return render(request, "alert.html", result)
    id = int(id)
    number = int(number)
    test = Test.objects.get(id=id)
    if test.test is None or test.test == b'':
        raise SuspiciousOperation("Некорректный запрос")
    asct_test = pickle.loads(test.test)
    if "type" in request.POST and int(request.POST["type"]) in (1, 2, 3):
        question_type = TestType(int(request.POST["type"]))

        if "question" in request.POST:
            question = Question(request.POST["question"], question_type)
        else:
            question = Question(None, question_type)

        if "image" in request.FILES:
            image = TestImage.objects.get_or_create(image=request.FILES["image"])
            question.set_image(image[0].id)
        else:
            question.set_image(asct_test.get_questions()[number - 1].get_image())

        if question_type is TestType.CLOSE_TYPE_SEVERAL_CORRECT_ANSWERS:
            i = 1
            while "answer" + str(i) in request.POST:
                question.add_new_answer(
                    CloseAnswer(
                        answer=request.POST["answer" + str(i)],
                        is_correct=str(i) in request.POST.getlist("trueAnswer")
                    )
                )
                i += 1
        elif question_type is TestType.CLOSE_TYPE_ONE_CORRECT_ANSWER:
            i = 1
            while "answer" + str(i) in request.POST:
                question.add_new_answer(
                    CloseAnswer(
                        answer=request.POST["answer" + str(i)],
                        is_correct=str(i) == request.POST["trueAnswer"]
                    )
                )
                i += 1
        elif question_type is TestType.OPEN_TYPE:
            question.add_new_answer(
                Answer(
                    request.POST["openAnswer"],
                    "checkManually" in request.POST
                )
            )

        asct_test.get_questions()[number - 1] = question
        test.test = pickle.dumps(asct_test)
        test.save()

        return HttpResponseRedirect(reverse("edit_test", args=[id]))
    else:
        question = asct_test.get_questions()[number - 1]
        if question.get_image():
            image_test = TestImage.objects.get(id=question.get_image())
            image = image_test.image.url
        else:
            image = None

        return render(
            request,
            "test/edit_question.html",
            {
                "number_of_question": number,
                "operation": "edit_test_edit_question",
                "type_list": TYPE_LIST,
                "test_id": id,
                "question": question,
                "image": image
            }
        )


@login_required
def delete_question(request, id):
    if request.user.user_type == UserProfile.PROBATIONER:
        result = {
            "status": "danger",
            "message": "Доступ запрещён"
        }
        return render(request, "alert.html", result)
    try:
        test = Test.objects.get(id=id)
    except:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    if test.test:
        exam_test = pickle.loads(test.test)
        if "delete" in request.POST:
            exam_test.get_questions().pop(int(request.POST["delete"]) - 1)
            test.test = pickle.dumps(exam_test)
            test.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def test_settings(request, id):
    if request.user.user_type == UserProfile.PROBATIONER:
        result = {
            "status": "danger",
            "message": "Доступ запрещён"
        }
        return render(request, "alert.html", result)
    try:
        test = Test.objects.get(id=id)
    except:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    journal_list = TestJournal.objects.filter(test=test)
    for journal in journal_list:
        if journal.date_to < timezone.now() - timezone.timedelta(days=1) and journal.status != TestJournal.COMPLETED and journal.status != TestJournal.OVERDUE:
            journal.status = TestJournal.OVERDUE
            journal.save()
    return render(
        request,
        "test/test_settings.html",
        {
            "test": test,
            "journal_list": journal_list
        }
    )


@login_required
def schedule_test(request, id):
    if request.user.user_type == UserProfile.PROBATIONER:
        result = {
            "status": "danger",
            "message": "Доступ запрещён"
        }
        return render(request, "alert.html", result)

    if "save" in request.POST:
        try:
            test = Test.objects.get(id=id)
            user = UserProfile.objects.get(id=request.POST["user"])
        except:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        scheduled_test = TestJournal.objects.create(
            date_to=datetime.datetime.strptime(request.POST["dateTo"], "%d.%m.%Y"),
            user=user,
            test=test
        )
        try:
            send_mail(
                'Вам назначен тест в ASCT',
                'Здравствуйте ' + user.first_name + '! \n \n Вам назначен тест: \"' + test.name + '\" \n\n Срок до ' +
                request.POST["dateTo"]
                + ' \n\n Для прохождения теста перейдите по ссылке: ' + request.build_absolute_uri(
                    reverse("start_test", args=[scheduled_test.id, ])),
                getattr(settings, "EMAIL_HOST_USER", None),
                [user.email],
                fail_silently=False
            )
        except:
            pass
        return HttpResponseRedirect(reverse("test_settings", args=[test.id, ]))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def edit_scheduled_test(request, id):
    try:
        scheduled_test = TestJournal.objects.get(id=id)
    except:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    if "dateTo" in request.POST:
        scheduled_test.date_to = datetime.datetime.strptime(request.POST["dateTo"], "%d.%m.%Y")
        if scheduled_test.status == TestJournal.OVERDUE:
            scheduled_test.status = TestJournal.ASSIGNED
        scheduled_test.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def cancel_test(request, id):
    if request.user.user_type == UserProfile.PROBATIONER:
        result = {
            "status": "danger",
            "message": "Доступ запрещён"
        }
        return render(request, "alert.html", result)
    try:
        TestJournal.objects.get(id=id).delete()
    except:
        pass
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def start_test(request, id):
    """
    Starts selected test
    :param request:
    :param id:
    :return:
    """
    try:
        journal = TestJournal.objects.get(id=id)
    except:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    if request.user.is_authenticated() and journal.user == request.user:
        progress = Progress.objects.filter(test_journal=journal)
        if not progress:
            Progress.objects.get_or_create(
                user=request.user,
                start_date=timezone.now(),
                end_date=None,
                test=journal.test,
                test_journal=journal,
                result_list=None,
                current_result=0
            )
        else:
            progress = progress[0]
            progress.start_date = timezone.now()
            progress.end_date = None
            progress.result_list = None
            progress.current_result = 0
            progress.save()
        return HttpResponseRedirect(reverse("next_question", args=[id, 1]))
    else:
        result = {
            "status": "danger",
            "message": "Доступ запрещён"
        }
        return render(request, "alert.html", result)


@login_required
def next_question(request, id, number):
    """
    Shows next question
    :param request:
    :param id: - id of test
    :param number: number of question
    :return:
    """
    id = int(id)
    number = int(number)
    journal = TestJournal.objects.get(id=id)
    progress = Progress.objects.filter(test_journal=journal)[0]
    result_list = []
    exam_test = pickle.loads(journal.test.test)

    if not progress.result_list:
        if number > 1:
            return HttpResponseRedirect(reverse("next_question", args=[journal.id, 1]))
    else:
        result_list = pickle.loads(progress.result_list)
        if len(result_list) > number - 1:
            return HttpResponseRedirect(reverse("next_question", args=[journal.id, len(result_list) + 1]))
        elif len(result_list) + 1 < number:
            return HttpResponseRedirect(reverse("next_question", args=[journal.id, len(result_list) + 1]))
        elif number > len(exam_test.get_questions()):
            return HttpResponseRedirect(reverse("index"))

    question = exam_test.get_questions()[number - 1]

    if "answer" in request.POST:
        is_correct = True
        check_manually = False
        request_answer = None
        if question.get_test_type() is TestType.OPEN_TYPE:
            if question.get_answers().get_check_manually():
                check_manually = True
                request_answer = request.POST["answer"]
            else:
                if question.get_answers().get_answer() != request.POST["answer"]:
                    is_correct = False
                    request_answer = request.POST["answer"]
                else:
                    request_answer = request.POST["answer"]
        elif question.get_test_type() is TestType.CLOSE_TYPE_SEVERAL_CORRECT_ANSWERS:
            correct_answer_list = []
            for item in range(len(question.get_answers())):
                if question.get_answers()[item].is_correct():
                    correct_answer_list.append(str(item + 1))
            is_correct = correct_answer_list == request.POST.getlist("answer")
            request_answer = request.POST.getlist("answer")
        elif question.get_test_type() is TestType.CLOSE_TYPE_ONE_CORRECT_ANSWER:
            correct_answer = 1
            for item in range(len(question.get_answers())):
                if question.get_answers()[item].is_correct():
                    correct_answer = item + 1
                    break
            is_correct = str(correct_answer) == request.POST["answer"]
            request_answer = request.POST["answer"]

        if is_correct and not check_manually:
            progress.current_result += 1
        result_list.append(
            AsctResult(
                is_correct=is_correct,
                answer=request_answer,
                check_manually=check_manually
            )
        )
        progress.result_list = pickle.dumps(result_list)
        progress.save()

        if number == len(exam_test.get_questions()):
            progress.end_date = timezone.now()
            progress.save()
            result_of_test = int(100 / len(exam_test.get_questions()) * progress.current_result)
            set_check_manually = False
            for result in result_list:
                if result.get_check_manually():
                    set_check_manually = True
            if set_check_manually:
                journal.status = TestJournal.CHECK_MANUALLY
            else:
                journal.status = TestJournal.COMPLETED
            journal.start_date = progress.start_date
            journal.end_date = progress.end_date
            journal.number_of_questions = len(exam_test.get_questions())
            journal.number_of_correct_answers = progress.current_result
            journal.result = result_of_test
            journal.report = progress.result_list
            journal.test_object = journal.test.test
            journal.save()

            return HttpResponseRedirect(reverse("end_test", args=[journal.id]))
        else:
            number += 1
            return HttpResponseRedirect(reverse("next_question", args=[journal.id, number]))

    progress = 100 / len(exam_test.get_questions()) * (number - 1)
    answers = question.get_answers()
    if question.get_image():
        image_test = TestImage.objects.get(id=question.get_image())
        image = image_test.image.url
    else:
        image = None
    if question.get_test_type() != TestType.OPEN_TYPE:
        variant_list = []
        for answer in answers:
            variant_list.append(answer.get_answer())
    else:
        variant_list = None

    return render(
        request,
        "test/next_question.html",
        {
            "journal": journal,
            "progress": progress,
            "number_of_question": number,
            "question": question.get_question(),
            "type": question.get_test_type().value,
            "variant_list": variant_list,
            "image": image
        }
    )


@login_required
def end_test(request, id):
    """
    Renders simple result form (without detail report)
    :param request:
    :param id: id of Journal field
    :return: end_test.html
    """
    journal = TestJournal.objects.get(id=id)
    if not journal:
        raise SuspiciousOperation("Некорректный запрос")
    elif not request.user.is_authenticated() and journal.user:
        raise SuspiciousOperation("Некорректный запрос")
    return render(
        request,
        "test/end_test.html",
        {
            "journal": journal,
            "check_manually": journal.status == TestJournal.CHECK_MANUALLY
        }
    )


@login_required
def report(request, id):
    """
    Prepares the report of the test result
    :param request:
    :param id: id of Journal field
    :return:
    """
    id = int(id)
    try:
        journal = TestJournal.objects.get(id=id)
    except:
        raise SuspiciousOperation("Некорректный запрос")
    if request.user.user_type == UserProfile.PROBATIONER and request.user != journal.user:
        result = {
            "status": "danger",
            "message": "Доступ запрещён"
        }
        return render(request, "alert.html", result)
    if not journal:
        raise SuspiciousOperation("Некорректный запрос")
    else:
        report = pickle.loads(journal.report)
        asct_test = pickle.loads(journal.test_object)
        return render(
            request,
            "test/report.html",
            {
                "journal": journal,
                "report": report,
                "exam_test": asct_test
            }
        )


@login_required
def check_manually_answer(request, id, number):
    """
    Shows next question
    :param request:
    :param id: - id of test
    :param number: number of question
    :return:
    """
    id = int(id)
    number = int(number)
    journal = TestJournal.objects.get(id=id)
    progress = Progress.objects.filter(test_journal=journal)[0]
    exam_test = pickle.loads(journal.test.test)
    result_list = pickle.loads(progress.result_list)

    if "True" in request.POST:
        is_correct = True
    else:
        is_correct = False

    if is_correct:
        progress.current_result += 1
    result_list[number] = AsctResult(
        is_correct=is_correct,
        answer=result_list[number].get_answer(),
        check_manually=False
    )

    progress.result_list = pickle.dumps(result_list)
    progress.save()

    result_of_test = int(100 / len(exam_test.get_questions()) * progress.current_result)
    set_check_manually = False
    for result in result_list:
        if result.get_check_manually():
            set_check_manually = True
    if set_check_manually:
        journal.status = TestJournal.CHECK_MANUALLY
    else:
        journal.status = TestJournal.COMPLETED
    journal.number_of_questions = len(exam_test.get_questions())
    journal.number_of_correct_answers = progress.current_result
    journal.result = result_of_test
    journal.report = progress.result_list
    journal.test_object = journal.test.test
    journal.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



@login_required
def schedule_test_to_user(request):
    if request.user.user_type == UserProfile.PROBATIONER:
        result = {
            "status": "danger",
            "message": "Доступ запрещён"
        }
        return render(request, "alert.html", result)
    if "save" in request.POST:
        try:
            test = Test.objects.get(id=request.POST["test"])
            user = UserProfile.objects.get(id=request.POST["user"])
        except:
            return HttpResponseRedirect(reverse("index"))
        scheduled_test = TestJournal.objects.create(
            date_to=datetime.datetime.strptime(request.POST["dateTo"], "%d.%m.%Y"),
            user=user,
            test=test
        )

        try:
            send_mail(
                'Вам назначен тест в ASCT',
                'Здравствуйте ' + user.first_name + '! \n \n Вам назначен тест: \"' + test.name + '\" \n\n Срок до ' +
                request.POST["dateTo"]
                + ' \n\n Для прохождения теста перейдите по ссылке: ' + request.build_absolute_uri(
                    reverse("start_test", args=[scheduled_test.id, ])),
                getattr(settings, "EMAIL_HOST_USER", None),
                [user.email],
                fail_silently=False
            )
        except:
            pass
        return HttpResponseRedirect(reverse("user_info", args=[user.id, ]))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def to_test_list(request, id):
    try:
        test = Test.objects.get(id=id)
    except:
        return HttpResponseRedirect(reverse("index"))
    return HttpResponseRedirect(reverse("journal_settings", args=[test.journal.id, ]))
