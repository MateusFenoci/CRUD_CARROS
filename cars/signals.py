from django.db.models.signals import pre_save, pre_delete, post_save, post_delete
from django.dispatch import receiver
from cars.models import Car, CarInventory
from django.db.models import Sum

def car_invetory_update():

    cars_counts = Car.objects.all().count()
    cars_value = Car.objects.aggregate(
        total_value = Sum('value')
    )['total_value']

    CarInventory.objects.create(
        cars_count=cars_counts,
        cars_value=cars_value,
    )


@receiver(pre_save, sender=Car)
def car_pre_save(sender, instance, **kwargs):
    if not instance.bio:
        instance.bio = 'Bio generica...'

@receiver(post_save, sender=Car)
def car_post_save(sender, instance, **kwargs):
    car_invetory_update()

@receiver(post_delete, sender=Car)
def car_post_delete(sender, instance, **kwargs):
   car_invetory_update()