# Third party imports.
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Local application imports.
from .models import Customer


# Creates profile for user immediately he/she registers.
@receiver(post_save, sender=User)
def create_cutomer_profile(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance)


# Saves user profile automatically after creating it.
@receiver(post_save, sender=User)
def save_customer_profile(sender, instance, **kwargs):
    instance.customer.save()
