from django.contrib import admin
from .models import Donor, Recipient, Organ, MatchedTransplantation,ContactSubmission

admin.site.register(Donor)
admin.site.register(Recipient)
admin.site.register(Organ)
admin.site.register(MatchedTransplantation)
@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "created_on")  # use custom column
    search_fields = ("name", "email", "message")
    # Remove any created_at filters if you don’t want time-based widgets
    # list_filter = ("created_at",)

    def created_on(self, obj):
        # Render only the date part in your preferred format
        # Example: 2025-08-18
        return obj.created_at.date().isoformat()
        # Or a custom format:
        # return obj.created_at.strftime("%b %d, %Y")   # e.g., Aug 18, 2025

    created_on.short_description = "Created on"
    created_on.admin_order_field = "created_at"  # still sort by the real field



# Register your models here.