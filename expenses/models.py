from datetime import datetime, timedelta
from django.db import models
from django.utils import timezone
from djmoney.models.fields import MoneyField, Money
from .deletable_model import DeletableModel
from util import truncate_string  # new line
from django.db.models import Q

# class ExpenseManager(models.Manager):
#     def active(self):
#         return self.filter(deleted=False)

#     # Soft delete only!
#     def delete_model(self, request, obj):
#         obj.deleted = True
#         obj.save()

#     def get_actions(self, request):
#         actions = super().get_actions(request)
#         # Remove the default delete action from the actions list
#         del actions["delete_selected"]
#         return actions

#     def soft_delete_selected(self, request, queryset):
#         # Mark selected entries as deleted (soft delete)
#         queryset.update(deleted=True)

#     soft_delete_selected.short_description = "Soft delete selected entries"

#     actions = [soft_delete_selected]


class TimesheetRate(DeletableModel):
    rate = MoneyField(
        decimal_places=3,
        default=0.000,
        default_currency="AUD",
        max_digits=11,
    )
    description = models.TextField(blank=True)
    default_rate = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.rate} {truncate_string(self.description,8)}"

    def save(self, *args, **kwargs):
        # Ensure that only one entry can be marked as a favorite
        if self.default_rate:
            TimesheetRate.objects.filter(~Q(pk=self.pk)).update(default_rate=False)
        super().save(*args, **kwargs)


class Timesheet(DeletableModel):
    shift_start = models.DateTimeField(null=True, blank=True)
    shift_end = models.DateTimeField(null=True, blank=True)
    break_start = models.DateTimeField(null=True, blank=True)
    break_end = models.DateTimeField(null=True, blank=True)
    submitted = models.DateTimeField(null=True, blank=True)
    rate = models.ForeignKey(
        TimesheetRate,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="timesheets",
    )

    @property
    def shift_hours(self) -> timedelta:
        if self.shift_start and self.shift_end:
            return self.shift_end - self.shift_start
        return timedelta(0)

    @property
    def break_hours(self) -> timedelta:
        if self.break_start and self.break_end:
            return self.break_end - self.break_start
        return timedelta(0)

    @property
    def worked_hours(self) -> timedelta:
        return self.shift_hours - self.break_hours

    @property
    def worked_decimal(self) -> str:
        return f"{self.worked_hours.total_seconds() / 60.0 / 60:.4f}"

    @property
    def total(self) -> Money:
        hours = self.worked_hours.total_seconds() / 60.0 / 60
        return hours * self.rate.rate

    def _rules(self):
        hours = self.worked_hours.total_seconds() / 60.0 / 60
        return hours > 3 and hours <= 7.5

    _rules.boolean = True
    rules = property(_rules)

    def __str__(self):
        return f"{self.shift_start} to {self.shift_end}"


class ExpenseCategory(DeletableModel):
    name = models.TextField(blank=True)
    description = models.TextField(blank=True)
    default_rate = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Expense(DeletableModel):
    price = MoneyField(
        decimal_places=3,
        default=0.000,
        default_currency="AUD",
        max_digits=11,
    )
    date = models.DateField()
    description = models.TextField(blank=True)
    merchant = models.CharField(max_length=255, blank=True)
    receipt = models.FileField(upload_to="receipts/", blank=True)
    link = models.URLField(blank=True)
    category = models.ForeignKey(
        ExpenseCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="expenses",
    )

    def __str__(self):
        return f"{self.date} {self.price} {truncate_string(self.description,32)}"
