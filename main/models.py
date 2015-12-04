from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from asct import settings


class UserProfileManager(BaseUserManager):
    def _create_user(self, email, date_of_birth, password,
                     is_superuser, **extra_fields):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('The users must have an email address')
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            date_of_birth=date_of_birth,
            is_active=True,
            is_superuser=is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, date_of_birth, password=None, **extra_fields):
        return self._create_user(email, date_of_birth, password, False,
                                 **extra_fields)

    def create_superuser(self, email, date_of_birth, password, **extra_fields):
        return self._create_user(email, date_of_birth, password, True,
                                 **extra_fields)


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

    def __str__(self):
        return self.name


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """
    The user-profile model
    """

    MALE = 'MALE'
    FEMALE = 'FEMALE'
    GENDER = (
        (MALE, 'MALE'),
        (FEMALE, 'FEMALE'),
    )

    CURATOR = 'CURATOR'
    ADMIN = 'ADMIN'
    OPERATOR = 'OPERATOR'
    PROBATIONER = 'PROBATIONER'
    USER_TYPE = (
        (CURATOR, 'CURATOR'),
        (ADMIN, 'ADMIN'),
        (OPERATOR, 'OPERATOR'),
        (PROBATIONER, 'PROBATIONER'),
    )

    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)

    # The additional attributes we wish to include.

    # The user's last name
    last_name = models.CharField(max_length=50)
    # The user's first name
    first_name = models.CharField(max_length=50)
    # The user's middle name
    middle_name = models.CharField(max_length=50)
    # The user's birthday
    date_of_birth = models.DateField()
    # Gender
    gender = models.CharField(max_length=6, choices=GENDER, default=MALE)
    # The user's profile photo
    photo = models.ImageField(upload_to='profile_photos', blank=True)
    # The company where the user works
    company = models.ForeignKey(Company, blank=True, null=True)
    # The department where the user works
    department = models.ForeignKey(Department, blank=True, null=True)
    # The user's job
    position = models.ForeignKey(Position, blank=True, null=True)
    # The user's registration date
    registration_date = models.DateTimeField(default=timezone.now)
    # user type
    user_type = models.CharField(max_length=11, choices=USER_TYPE, default=CURATOR)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['date_of_birth']

    def get_full_name(self):
        return self.last_name + ' ' + self.first_name + ' ' + self.middle_name

    def get_short_name(self):
        return self.first_name + ' ' + self.last_name

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_superuser


class Journal(models.Model):
    # The name of journal
    name = models.CharField(max_length=500)
    # The description of theme
    description = models.TextField(blank=True)
    # The owner of journal
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    # Company
    company = models.ForeignKey(Company, blank=True, null=True)



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

    # The user, who was complete the test
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
    # The completed test
    test = models.ForeignKey(Test)
    # Date and time of start test
    start_date = models.DateTimeField(default=timezone.now)
    # Date and time of end test
    end_date = models.DateTimeField(default=timezone.now)
    # Number of questions
    number_of_questions = models.IntegerField()
    # Number of correct answers
    number_of_correct_answers = models.IntegerField(default=0)
    # The result of test (%)
    result = models.IntegerField(default=0)
    # The report of the test (JSON - file)'
    report = models.BinaryField()
    # The test
    test_object= models.BinaryField()

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

