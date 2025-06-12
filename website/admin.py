from django.contrib import admin
from .models import Service, Technology, Project, ContactMessage

# Register your models with the Django admin site
admin.site.register(Service)
admin.site.register(Technology)
admin.site.register(Project)
admin.site.register(ContactMessage)