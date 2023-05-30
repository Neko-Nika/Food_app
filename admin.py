from django.contrib import admin

# Register your models here.
import app.models

admin.site.register(app.models.Profile)
admin.site.register(app.models.Reminders)
admin.site.register(app.models.Day)
admin.site.register(app.models.Meal)
