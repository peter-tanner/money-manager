from django.db import models
from simple_history.models import HistoricalRecords


class DeletableModel(models.Model):
    class Meta:
        abstract = True

    history = HistoricalRecords(inherit=True)
    deleted = models.BooleanField(default=False)

    def mark_deleted(self):
        self.deleted = True
