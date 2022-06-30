from django.contrib import admin
from .models import otp, HomeworkUploads, Preferences, Notifications, Quotes, Question, Note


# Register your models here.

admin.site.register(otp)
admin.site.register(HomeworkUploads)
admin.site.register(Preferences)
admin.site.register(Notifications)
admin.site.register(Quotes)
admin.site.register(Question)
admin.site.register(Note)
