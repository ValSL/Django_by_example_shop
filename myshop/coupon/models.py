from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Coupon(models.Model):
    code = models.CharField(max_length=50,
                            unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(validators=[MaxValueValidator(100), MinValueValidator(0)])
    active = models.BooleanField()

    def __str__(self):
        return self.code
