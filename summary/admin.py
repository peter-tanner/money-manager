from django.contrib import admin
from .models import SaleSummary
from django.db.models import (
    Sum,
    Count,
    F,
    ExpressionWrapper,
    DecimalField,
    DurationField,
    FloatField,
)
from djmoney.models.fields import MoneyField
from django.db.models.functions import TruncMonth


@admin.register(SaleSummary)
class SaleSummaryAdmin(admin.ModelAdmin):
    change_list_template = "admin/sale_summary_change_list.html"
    date_hierarchy = "shift_start"

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )

        try:
            qs = response.context_data["cl"].queryset
        except (AttributeError, KeyError):
            return response

        metrics = {
            "month": TruncMonth("shift_start"),
            "total": Sum(F("shift_end") - F("shift_start")),
            "total_sales": Sum(
                ExpressionWrapper(
                    (F("shift_end") - F("shift_start"))
                    / 60.0
                    / 1000000
                    / 60
                    * F("rate__rate"),
                    # MoneyField does not work https://github.com/django-money/django-money/issues/627
                    output_field=DecimalField(),
                )
            ),
        }

        response.context_data["summary"] = list(
            qs.values("shift_start__month").annotate(**metrics).order_by("month")
        )

        metrics.pop("month")
        response.context_data["summary_total"] = dict(qs.aggregate(**metrics))
        return response
