from django.db import models
from django.contrib.auth.models import User
import uuid
# Create your models here.
class BaseModel(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    created_at = models.DateField(auto_now = True)
    Updated_at = models.DateField(auto_now_add = True)

    class Meta:
        abstract = True


class Transaction(BaseModel):
    description = models.CharField(max_length=100, blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    Created_by = models.ForeignKey(User, on_delete = models.CASCADE, blank=True, null=True)

    class Meta:
        ordering = ('description',)

    def isNegative(self):
        return self.amount < 0 # it refer to Transaction model amount field(see above line 13 ⬆️).