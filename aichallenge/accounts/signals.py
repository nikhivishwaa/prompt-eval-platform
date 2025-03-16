from accounts.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver
from worker.profile_worker import delete_pic
import random as rd
import asyncio


# @receiver(pre_save, sender=User)
# def handle_profile_pic(sender, instance=None, **kwargs):
#     if instance.id is not None and instance.profile_pic.name:
#         print('profile_pic added:',instance.id, instance.profile_pic.name)
#         original = User.objects.get(pk=instance.pk)
#         pic = instance.profile_pic
#         if pic.name != original.profile_pic.name:
#             # Perform your specific action here
#             if pic.file.size // 1024 < 100:
#                 old_pic = original.profile_pic
#                 num = 10**4
#                 pk = instance.pk
#                 instance.profile_pic.name = f'user/xu-{pk}-0{num - pk * pk // 10 ** 2 }/profile/pic-{pic.name[-30:]}'
#                 print("Attribute 'profile_pic' has been modified.")
#                 asyncio.run(delete_pic(old_pic))
#             else:
#                 instance.profile_pic = original.profile_pic


