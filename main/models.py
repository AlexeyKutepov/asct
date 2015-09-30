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
    company = models.CharField(max_length=500, blank=True)
    # The department where the user works
    department = models.CharField(max_length=500, blank=True)
    # The user's job
    position = models.CharField(max_length=500, blank=True)
    # The user's registration date
    registration_date = models.DateTimeField(default=timezone.now())

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


class Exam(models.Model):
    pass


class SubTheme(models.Model):
    # The name of theme
    name = models.CharField(max_length=500)
    # The description of theme
    description = models.TextField(blank=True)
    # The owner of journal
    owner = models.OneToOneField(settings.AUTH_USER_MODEL)
    # The sub themes to study
    exam = models.OneToOneField(Exam, blank=True, null=True)


class Theme(models.Model):
    # The name of theme
    name = models.CharField(max_length=500)
    # The description of theme
    description = models.TextField(blank=True)
    # The owner of journal
    owner = models.OneToOneField(settings.AUTH_USER_MODEL)
    # The sub themes to study
    sub_theme = models.ForeignKey(SubTheme, blank=True, null=True)


class Journal(models.Model):
    # The name of journal
    name = models.CharField(max_length=500)
    # The owner of journal
    owner = models.OneToOneField(settings.AUTH_USER_MODEL)
    # The themes to study
    theme = models.ForeignKey(Theme, blank=True, null=True)