from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Poll)
admin.site.register(Poll_Question_Options)
admin.site.register(Poll_Question_Responses)
admin.site.register(Poll_Questions)


