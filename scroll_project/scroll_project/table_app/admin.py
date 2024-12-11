from django.contrib import admin
from .models import TableRow

@admin.register(TableRow)
class TableRowAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'details', 'created_at')  # Fields to display in the admin list view
    list_filter = ('created_at',)  # Add filter options
    search_fields = ('name', 'details')  # Add search functionality
    ordering = ('-created_at',)  # Default ordering
