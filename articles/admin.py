# Path: articles/admin.py

from django.contrib import admin
from django.utils.html import format_html
from .models import Article, Reaction

admin.site.register(Reaction)


@admin.action(description="Approve selected articles")
def approve(modeladmin, request, queryset):
    queryset.update(status='Approved')


@admin.action(description="Reject selected articles")
def reject(modeladmin, request, queryset):
    queryset.update(status='Rejected')


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'specialization', 'colored_status', 'created_at']
    
    list_filter = ['status', 'specialization', 'created_at']
    
    search_fields = ['title', 'content', 'author__user__username']
    
    actions = [approve, reject]
    
    list_select_related = ['author', 'author__user', 'specialization']

    def colored_status(self, obj):
        colors = {
            'Approved': '#2ecc71',  # أخضر مريح للعين
            'Rejected': '#e74c3c',  # أحمر واضح
            'Pending': '#e67e22'   # برتقالي للتنبيه
        }
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            colors.get(obj.status, 'black'),
            obj.status
        )
    
    colored_status.short_description = 'Status'