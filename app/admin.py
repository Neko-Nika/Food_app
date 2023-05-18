from django.contrib import admin

# Register your models here.
import app.models

admin.site.register(app.models.Profile)
admin.site.register(app.models.Reminders)