from django.db import models
from django.utils import timezone
from asct import settings


class Company(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name


class Position(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.TextField()
    company = models.ForeignKey(Company)
    position = models.ManyToManyField(Position, blank=True)

    def __str__(self):
        return self.name


class Journal(models.Model):
    # The name of journal
    name = models.CharField(max_length=500)
    # The description of theme
    description = models.TextField(blank=True)
    # The owner of journal
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    # Company
    company = models.ForeignKey(Company, blank=True, null=True)
    # Department
    department = models.ForeignKey(Department, blank=True, null=True)


class Theme(models.Model):
    # The name of theme
    name = models.CharField(max_length=500)
    # The description of theme
    description = models.TextField(blank=True)
    # The owner of theme
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    # The journal
    journal = models.ForeignKey(Journal, blank=True, null=True)


class ScheduledTheme(models.Model):
    ASSIGNED = 'ASSIGNED'
    IN_WORK = 'IN_WORK'
    COMPLETED = 'COMPLETED'
    OVERDUE = 'OVERDUE'
    STATUS = (
        (ASSIGNED, 'ASSIGNED'),
        (IN_WORK, 'IN_WORK'),
        (COMPLETED, 'COMPLETED'),
    )
    # Start date
    date_from = models.DateTimeField(default=timezone.now)
    # End date
    date_to = models.DateTimeField(default=timezone.now)
    # Status
    status = models.CharField(max_length=10, choices=STATUS, default=ASSIGNED)
    # User
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    #Theme
    theme = models.ForeignKey(Theme)
    # Progress
    progress = models.IntegerField(default=0)


class ThemeExam(models.Model):
    # The owner of exam
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='themeexam_users')
    # The owner of exam
    examiner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='themeexam_examiners')
    # Theme
    theme = models.ForeignKey(Theme)
    # Date of exam
    datetime = models.DateTimeField(default=timezone.now)
    # Place
    place = models.TextField(blank=True, null=True)
    # The result
    result = models.FloatField(blank=True, null=True)


class SubTheme(models.Model):
    # The name of theme
    name = models.CharField(max_length=500)
    # The description of theme
    description = models.TextField(blank=True)
    # The owner of theme
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    # The parent theme to study
    parent_theme = models.ForeignKey(Theme, blank=True, null=True)


class ScheduledSubTheme(models.Model):
    ASSIGNED = 'ASSIGNED'
    IN_WORK = 'IN_WORK'
    COMPLETED = 'COMPLETED'
    STATUS = (
        (ASSIGNED, 'ASSIGNED'),
        (IN_WORK, 'IN_WORK'),
        (COMPLETED, 'COMPLETED'),
    )
    # Start date
    date_from = models.DateTimeField(default=timezone.now)
    # End date
    date_to = models.DateTimeField(default=timezone.now)
    # User
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    #Sub theme
    sub_theme = models.ForeignKey(SubTheme)
    # Status
    status = models.CharField(max_length=10, choices=STATUS, default=ASSIGNED)
    # Parent
    scheduled_theme = models.ForeignKey(ScheduledTheme)


class File(models.Model):
    # File
    file = models.FileField(upload_to='files')
    # Theme
    theme = models.ForeignKey(Theme, blank=True, null=True)
    # Sub theme
    sub_theme = models.ForeignKey(SubTheme, blank=True, null=True)

    def __str__(self):
        return self.file.name[6:]

