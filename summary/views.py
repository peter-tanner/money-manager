# from django.shortcuts import render
# from django.db.models import Sum, F
# from .models import TimesheetSummary
# from expenses.models import Timesheet  # Adjust the import as needed


# def summary_dashboard(request):
#     # Calculate summary data (example: total hours and total sales per month)
#     summary_data = (
#         Timesheet.objects.values("shift_start__month", "shift_start__year")
#         .annotate(
#             total_hours=Sum(F("shift_end") - F("shift_start")),
#             total_sales=Sum("id"),
#         )
#         .order_by("-shift_start__year", "-shift_start__month")
#     )

#     # Save or update the summary data in the TimesheetSummary model
#     for data in summary_data:
#         month = data["shift_start__month"]
#         year = data["shift_start__year"]
#         total_hours = data["total_hours"]
#         total_sales = data["total_sales"]

#         # # Use get_or_create to avoid duplicates
#         # summary_obj, _ = TimesheetSummary.objects.get_or_create(
#         #     month=month,
#         #     year=year,
#         #     defaults={"total_hours": total_hours, "total_sales": total_sales},
#         # )
#     context = {"summary_data": TimesheetSummary.objects.all()}
#     return render(request, "admin/summary/summary_dashboard.html", context)
