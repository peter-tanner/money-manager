from django.db import models
from expenses.models import Timesheet


class SaleSummary(Timesheet):
    class Meta:
        proxy = True
        verbose_name = "Sale Summary"
        verbose_name_plural = "Sales Summary"
