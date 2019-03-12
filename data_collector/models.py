from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
class DataPoint(models.Model):
    node_name = models.CharField(max_length = 250)
    datetime = models.DateTimeField(auto_now_add = True)

    data_type = models.CharField(max_length = 100)
    data_value = models.FloatField()

    def __str__(self):
        return 'DataPoint for {}, {} = {}'.format(
            self.node_name,
            self.data_type,
            self.data_value
        )

class Alert(models.Model):
    data_type = models.CharField(max_length = 100)
    min_value = models.FloatField(null=True, blank=True)
    max_value = models.FloatField(null=True, blank=True)
    node_name = models.CharField(max_length=250, blank = True)

    is_active = models.BooleanField(default=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.min_value is None and self.max_value is None:
            raise ValidationError('max_value and min_value can\'t be empty')
        return super(Alert, self).save()