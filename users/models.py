from django.contrib.auth.models import AbstractUser
from django.db import models


# TODO - we need to now the schema from google places api
class Address(models.Model):
    country = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    street = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=6)
    house_number = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.country} - {self.city} - {self.street} - {self.house_number}"


class User(AbstractUser):
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    addresses = models.ForeignKey(
        Address, on_delete=models.CASCADE, null=True, blank=True
    )

    def can_make_order(self) -> bool:
        """Check if there are Enough Information about the User or Not to Make an Order
        - Check one Contact way at least is filled (phone_number , email)
        - Check if the user has an address
        """

        if self.phone_number or self.email:
            if self.addresses:
                return True
        return False
