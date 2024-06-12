from django.contrib import admin
from .models import TransectionLog, Wallet, TransectionRequest


admin.site.register(TransectionLog)
admin.site.register(Wallet)
admin.site.register(TransectionRequest)
