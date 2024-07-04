from django.contrib import admin
from .models import DriverCar, Car, BasePercent, BaseTimeRefund


admin.site.register(DriverCar)
admin.site.register(Car)
admin.site.register(BasePercent)
admin.site.register(BaseTimeRefund)
