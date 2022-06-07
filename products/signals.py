from django.db.models.signals import post_delete  , pre_save
from django.dispatch import receiver
from .models import ProductImage
from core.storages import select_storage

@receiver(post_delete, sender=ProductImage)
def my_handler(sender,instance:ProductImage, **kwargs):
    """delete the image file after Deleting the Object in Database """
    storage = select_storage()
    file_name = instance.image.name 
    if storage.exists(file_name):
      storage.delete(file_name)


@receiver(pre_save, sender=ProductImage)
def pre_save_handeler(sender,instance:ProductImage, **kwargs):
    """Delete the Old file if there is Before save the New one"""
    storage = select_storage()
    qs = ProductImage.objects.filter(id=instance.id) or None
    if qs:
      obj = qs.first()
      file_name = obj.image.name
      if storage.exists(file_name):
        storage.delete(file_name)



