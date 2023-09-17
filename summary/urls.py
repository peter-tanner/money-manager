from django.urls import path
from . import admin

urlpatterns = [
    path("summary/", admin.SaleSummaryAdmin, name="summary_dashboard"),
]
