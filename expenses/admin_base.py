from simple_history.admin import SimpleHistoryAdmin
from .deletable_model import DeletableModel
from django.utils.html import format_html
from django.contrib import admin
from django import forms


class DeletedListFilter(admin.BooleanFieldListFilter):
    default = "0"

    def __init__(self, field, request, params, model, model_admin, field_path):
        super().__init__(field, request, params, model, model_admin, field_path)
        if not self.lookup_val:
            self.lookup_val = self.default
            self.used_parameters[self.lookup_kwarg] = self.default

    def choices(self, changelist):
        choices = super().choices(changelist)
        choices.__next__()
        for choice in choices:
            yield choice


class DeletableAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.deleted:
            # If the object is marked as deleted, add your custom action button
            self.fields["restore_deleted"] = forms.BooleanField(
                widget=forms.CheckboxInput(attrs={"class": "hidden"}),
                required=False,
                initial=True,
                label="Restore This Item",
            )


class AdminBase(SimpleHistoryAdmin):
    readonly_fields = ("deleted",)

    # Override the delete_view method to suppress the confirmation page
    def delete_view(self, request, object_id, extra_context=None):
        obj: DeletableModel = self.get_object(request, object_id)
        if obj:
            obj.mark_deleted()
            obj.save()
        return self.response_delete(request, obj_display=str(obj), obj_id=obj.pk)

    # Override delete button
    def delete_model(self, request, obj: DeletableModel):
        if obj:
            obj.mark_deleted()
            obj.save()

    def delete_selected(modeladmin, request, queryset):
        # Show confirmation page.
        for obj in queryset:
            if obj:
                obj.mark_deleted()
                obj.save()

    def restore_deleted(self, request, queryset):
        # Check if the selected items are deleted
        deleted_items = queryset.filter(deleted=True)

        # Perform the action only if there are deleted items
        if deleted_items.exists():
            # Your custom logic here
            for item in deleted_items:
                item.deleted = False
                item.save()

    restore_deleted.short_description = "Restore Selected Items"  # Action button text

    # Add your custom action to the actions list
    actions = [delete_selected, restore_deleted]

    """
    HISTORY
    https://stackoverflow.com/a/72187314
    """
    history_list_display = ["list_changes"]

    def changed_fields(self, obj):
        if obj.prev_record:
            delta = obj.diff_against(obj.prev_record)
            return delta.changed_fields
        return None

    def list_changes(self, obj):
        fields = ""
        if obj.prev_record:
            delta = obj.diff_against(obj.prev_record)

            for change in delta.changes:
                fields += str(
                    (
                        f"<strong>{change.field}</strong> "
                        f"changed from <span style='background-color:#ffb5ad'>{change.old}</span> "
                        f"to <span style='background-color:#b3f7ab'>{change.new}</span> . <br/>"
                    )
                )
            return format_html(fields)
        return None
