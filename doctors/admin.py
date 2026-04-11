from django.contrib import admin
from .models import Doctor , Education , PaymentMethod, Schedule, Specialties, job_title
from django.utils.html import format_html
# Register your models here.

Models = [
    Doctor,
    Schedule,
    PaymentMethod,
    Specialties,
    job_title,
]

admin.site.register(Models)

@admin.action(description="Approve selected certificates")
def approve_certificates(modeladmin, request, queryset):
    for obj in queryset:
        obj.status = 'approved'
        obj.save()

@admin.action(description="Reject selected certificates")
def reject_certificates(modeladmin, request, queryset):
    for obj in queryset:
        obj.status = 'rejected'
        obj.save()

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin): 
    list_display = ['doctor', 'degree', 'institution', 'status' , 'created_at', 'view_certificate']
    list_filter = ['status']
    actions = [approve_certificates, reject_certificates]
    
    search_fields = ['doctor__user__username', 'degree', 'institution']

    def view_certificate(self, obj):
        if obj.certificate:
            return format_html(
                '<a href="{}" target="_blank">📄 View Certificate</a>',
                obj.certificate.url
            )
        return "No File"
 
