from django.db import models
from django.contrib.auth.models import UserManager, AbstractUser
from main.models import Company, Position, Department
from django.utils import timezone


class UserProfile(AbstractUser):
    """
    The user-profile model
    """

    MALE = 'MALE'
    FEMALE = 'FEMALE'
    GENDER = (
        (MALE, 'MALE'),
        (FEMALE, 'FEMALE'),
    )

    ADMIN = 'ADMIN'
    OPERATOR = 'OPERATOR'
    PROBATIONER = 'PROBATIONER'
    USER_TYPE = (
        (ADMIN, 'ADMIN'),
        (OPERATOR, 'OPERATOR'),
        (PROBATIONER, 'PROBATIONER'),
    )
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
    user_type = models.CharField(max_length=11, choices=USER_TYPE, default=ADMIN)

    objects = UserManager()

    def get_full_name(self):
        return self.last_name + ' ' + self.first_name + ' ' + self.middle_name

    def get_short_name(self):
        return self.first_name + ' ' + self.last_name
