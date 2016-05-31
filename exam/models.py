from django.db import models
from django.utils import timezone
from asct import settings
from main.models import Journal


class Test(models.Model):
    """
    The model of the test
    """

    # The name of the test
    name = models.CharField(max_length=500)
    # The description of test
    description = models.TextField(blank=True)
    # Journal
    journal = models.ForeignKey(Journal, blank=True, null=True)
    # The test
    test = models.BinaryField(blank=True)
    # The author of the test
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    # date and time of create test
    date_and_time = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return self.name


class TestJournal(models.Model):
    """
    The result journal
    """
    ASSIGNED = 'ASSIGNED'
    COMPLETED = 'COMPLETED'
    CHECK_MANUALLY = 'CHECK_MANUALLY'
    OVERDUE = 'OVERDUE'
    STATUS = (
        (ASSIGNED, 'ASSIGNED'),
        (COMPLETED, 'COMPLETED'),
        (CHECK_MANUALLY, 'CHECK_MANUALLY'),
        (OVERDUE, 'OVERDUE'),
    )
    # The user, who was complete the test
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
    # The completed test
    test = models.ForeignKey(Test)
    date_from = models.DateTimeField(default=timezone.now)
    date_to = models.DateTimeField(default=timezone.now)
    # Date and time of start test
    start_date = models.DateTimeField(default=timezone.now)
    # Date and time of end test
    end_date = models.DateTimeField(default=timezone.now)
    # Number of questions
    number_of_questions = models.IntegerField(blank=True, null=True)
    # Number of correct answers
    number_of_correct_answers = models.IntegerField(default=0)
    # The result of test (%)
    result = models.IntegerField(default=0)
    # The report of the test (JSON - file)'
    report = models.BinaryField(blank=True, null=True)
    # The test
    test_object= models.BinaryField(blank=True, null=True)
    # Status
    status = models.CharField(max_length=10, choices=STATUS, default=ASSIGNED)

    def __str__(self):
        if self.user:
            return self.user.get_full_name()
        else:
            return "Unknown"


class Progress(models.Model):
    """
    The progress of the performing tests by users
    """

    # The user, who  performs the test
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
    # Start date time
    start_date = models.DateTimeField(default=timezone.now)
    # End date time
    end_date = models.DateTimeField(blank=True, null=True)
    # The performed test by user
    test = models.ForeignKey(Test)
    # The current result
    result_list = models.BinaryField(blank=True, null=True)
    # Number of correct answers
    current_result = models.IntegerField(default=0)


class TestImage(models.Model):
    """
    There are images for tests
    """
    image = models.ImageField(upload_to='test_images', blank=True)

