from django.shortcuts import render

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from .models import Expense


def restore_item(request, item_id):
    try:
        item = Expense.objects.get(pk=item_id)
        item.deleted = False
        item.save()
        messages.success(request, "Item restored successfully.")
    except Expense.DoesNotExist:
        messages.error(request, "Item not found.")
    return HttpResponseRedirect(reverse("admin:expenses_expense_changelist"))
