from django.urls import path
from . import views

app_name = "expenses"

urlpatterns = [
    path(
        "expense/<int:item_id>/restore/",
        views.restore_item,
        name="expenses_restore_item",
    ),
]
