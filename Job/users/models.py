from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _
from PIL import Image
from ckeditor.fields import RichTextField
from django.dispatch import receiver


# Create your models here.

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('your email is not correct!')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_super', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_super = True')

        return self._create_user(email, password, **extra_fields)


class Account(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=50, blank=False)
    last_name = models.CharField(_('last name'), max_length=50, blank=False)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('is_staff'), default=False)
    is_employee = models.BooleanField(default=False)
    is_employer = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_profile_id(self):
        return self.profile.id


class Profile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE, related_name="profile")
    image = models.ImageField(upload_to="media/users", default="media/users/person_1.jpg")
    birth_day = models.DateTimeField(default=None, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True)
    resume = RichTextField(blank=True)
    company = models.CharField(max_length=250, blank=True)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name + " " + self.user.email

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
        img = Image.open(self.image)
        if img.height > 200 or img.width > 200:
            new_size = (200, 200)
            img.thumbnail(new_size)
            img.save(self.image.path)


@receiver(models.signals.post_save, sender=Account)
def post_save_user_signal(sender, instance, created, **kwargs):
    if created:
        instance.save()


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


post_save.connect(create_user_profile, sender=Account)
