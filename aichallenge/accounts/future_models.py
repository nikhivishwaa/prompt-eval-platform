# from django.db import models
# from django.contrib.auth.models import AbstractUser
# from .manager import UserManager
# from django.core.validators import EmailValidator
# from accounts.helpers import validators as v
# import datetime as dt



# class Role(models.Model):
#     role_name = models.CharField(max_length=30, blank=True)
#     role_desc = models.TextField(null=True, blank=True, max_length=300)
#     role_level = models.IntegerField(null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     # permissions
#     can_predict = models.BooleanField(default=False)
#     view_dataset = models.BooleanField(default=False)
#     modify_dataset = models.BooleanField(default=False)
#     batch_prediction = models.BooleanField(default=False)
#     create_org = models.BooleanField(default=False)
#     join_org = models.BooleanField(default=False)
#     multi_org = models.BooleanField(default=False)

#     class Meta:
#         verbose_name_plural = 'User Roles'
#         ordering = ['role_name', 'role_level']
#         unique_together = (
#                             'can_predict', 'batch_prediction', 
#                             'view_dataset', 'modify_dataset',
#                             'create_org', 'join_org', 'multi_org'
#                         )
#     def __str__(self):
#         return self.role_name


# class User(AbstractUser):
#     GENDER = (
#         ('m', 'Male'),
#         ('f', 'Female'),
#         ('x', 'Other')
#     )
#     username = None
#     # profile data
#     email = models.EmailField(unique=True, validators=[EmailValidator, v.validate_email])
#     phone = models.CharField(max_length=10, unique=True, validators=[v.validate_phone_number])
#     first_name = models.CharField(max_length=150, validators=[v.validate_first_name])
#     last_name = models.CharField(max_length=150, blank=True, validators=[v.validate_last_name])
#     gender = models.CharField(max_length=10, blank=True, choices=GENDER)
#     dob = models.DateField(blank=True, null=True)
#     profile_pic = models.FileField(upload_to='media/user/profile', null=True, blank=True)
#     last_modified = models.DateField(auto_now=True)
#     # verification detail
#     verified = models.BooleanField(default=False)
#     email_otp = models.CharField(max_length=6,blank=True, null=True)
#     email_otp_ts = models.DateTimeField(blank=True, null=True)
#     email_verified_at = models.DateTimeField(blank=True, null=True)
#     phone_otp = models.CharField(max_length=6,blank=True, null=True)
#     phone_otp_ts = models.DateTimeField(blank=True, null=True)
#     phone_verified_at = models.DateTimeField(blank=True, null=True)
#     # forgot password
#     fget_otp = models.CharField(max_length=6,blank=True, null=True)
#     fget_token = models.CharField(max_length=100, null=True, blank=True)
#     fget_otp_ts = models.DateTimeField(blank=True, null=True)
#     last_fget = models.DateTimeField(blank=True, null=True)
#     # role, organization and suspension
#     # role = models.ForeignKey(Role, on_delete=models.PROTECT, null=True, blank=True)
#     suspended = models.BooleanField(default=True)

#     objects = UserManager()

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['phone_number', 'first_name']

    
#     class Meta:
#         db_table = "Users"
#         verbose_name = "User"

#     def __str__(self):
#         return f'{self.email} : {self.first_name}'


# class Organization(models.Model):
#     org_name = models.CharField(max_length=30)
#     org_address = models.TextField(max_length=300)
#     onboard_date = models.DateField(auto_now_add=True)
#     stablish_date = models.DateField()
#     # org verification
#     documents = models.FileField(blank=True, upload_to='media/org/documents')
#     verified = models.BooleanField(default=False)
#     verified_at = models.DateTimeField(null=True, blank=True)
#     # admin
#     org_admin = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)

#     class Meta:
#         verbose_name_plural = 'Organization'
#         ordering = ['org_admin', 'org_name']

#     def __str__(self):
#         return self.role_name


# class OrgMembers(models.Model):
#     position = models.CharField(max_length=50)
#     assign_date = models.DateField(auto_now_add=True)
#     stablish_date = models.DateField(blank=True)
#     manager = models.ForeignKey(OrgMembers, on_delete=models.PROTECT, null=True, blank=True)
#     # part of org
#     active = models.BooleanField(default=False)
#     last_login = models.DateTimeField(blank=True)
#     removed = models.BooleanField(default=False)
#     # org and their member
#     member = models.ForeignKey(User, on_delete=models.CASCADE)
#     org = models.ForeignKey(Organization, on_delete=models.CASCADE)
#     role = models.ForeignKey(Role, on_delete=models.PROTECT, null=True, blank=True)

#     class Meta:
#         verbose_name_plural = 'Org Members'
#         ordering = ['position']
#         unique_together = ('org', 'member')

#     def __str__(self):
#         return self.role_name

