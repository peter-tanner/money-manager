from datetime import datetime
from typing import Any, Dict
from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from django.core.handlers.wsgi import WSGIRequest
from django.db.models.base import Model
from django.db.models.fields import Field
from django.forms import DecimalField, TextInput, NumberInput
from django.db import models

from util import next_payday

from .admin_base import AdminBase, DeletedListFilter, DeletableAdminForm
from .models import Expense, Timesheet, TimesheetRate
from django import forms
from django.utils import timezone
from django.contrib.admin.widgets import AdminDateWidget, AdminSplitDateTime
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from admincharts.admin import AdminChartMixin
from admincharts.utils import months_between_dates
from djmoney.contrib.exchange.models import convert_money


class TimesheetRateAdminForm(DeletableAdminForm):
    class Meta:
        model = TimesheetRate
        fields = "__all__"


@admin.register(TimesheetRate)
class TimesheetRateAdmin(AdminBase):
    list_display = (
        "rate",
        "description",
        "default_rate",
    )
    form = TimesheetRateAdminForm


class TimesheetResource(resources.ModelResource):
    class Meta:
        model = Timesheet


class TimesheetAdminForm(DeletableAdminForm):
    class Meta:
        model = Timesheet
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.shift_start:
            self.initial["shift_start"] = timezone.now()
        self.fields["rate"].initial = forms.ModelChoiceField(
            queryset=TimesheetRate.objects.all(),
            required=True,
            widget=forms.Select,
            label="Select Another Table",
        )
        self.initial["rate"] = TimesheetRate.objects.filter(default_rate=True).first()


@admin.register(Timesheet)
class TimesheetAdmin(AdminBase, AdminChartMixin, ImportExportModelAdmin):
    resource_classes = [TimesheetResource]
    form = TimesheetAdminForm
    fields = (
        ("shift_start", "shift_end"),
        ("break_start", "break_end"),
        ("rate"),
        ("submitted"),
    )

    list_display = (
        "shift_start",
        "worked_hours",
        "worked_decimal",
        "total",
        "_rules",
        "submitted",
        "rate",
        # "shift_hours",
        # "break_hours",
    )
    list_filter = ("shift_start", ("deleted", DeletedListFilter))
    ordering = ("-shift_start", "-deleted")
    readonly_fields = ("deleted",)

    def submit(self, request, queryset):
        if queryset.exists():
            for item in queryset:
                if not item.submitted:
                    item.submitted = timezone.now()
                    item.save()

    def changelist_view(self, request, extra_context=None):
        payday = next_payday()
        extra_context = {
            "title": f"Next timesheet due {payday.strftime('%B %-d')} (in {(payday - datetime.now()).days + 1} days)."
        }
        return super().changelist_view(request, extra_context=extra_context)

    submit.short_description = "Mark as submitted"

    actions = [submit, AdminBase.delete_selected, AdminBase.restore_deleted]

    def get_list_chart_data(self, queryset):
        if not queryset:
            return {}

        # Cannot reorder the queryset at this point
        earliest = min([x.shift_start for x in queryset])

        labels = []
        totals = []
        for b in months_between_dates(earliest, timezone.now()):
            labels.append(b.strftime("%b %Y"))
            totals.append(
                sum(
                    [
                        convert_money(x.total, "AUD").amount
                        for x in queryset
                        if x.shift_start.year == b.year
                        and x.shift_start.month == b.month
                    ]
                )
            )

        return {
            "labels": labels,
            "datasets": [
                {
                    "label": "Income (Pre-tax)",
                    "data": totals,
                    "backgroundColor": "#79aec8",
                },
            ],
        }


class ExpenseAdminForm(DeletableAdminForm):
    class Meta:
        model = Expense
        fields = "__all__"


@admin.register(Expense)
class ExpenseAdmin(AdminBase, AdminChartMixin, ImportExportModelAdmin):
    form = ExpenseAdminForm

    list_display = ("date", "price", "description")
    list_filter = ("date", ("deleted", DeletedListFilter))
    ordering = ("-date", "-deleted")
    readonly_fields = ("deleted",)

    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        initial["date"] = timezone.now().date()
        return initial

    list_chart_type = "bar"
    list_chart_data = {}
    list_chart_options = {"aspectRatio": 6}
    list_chart_config = None  # Override the combined settings