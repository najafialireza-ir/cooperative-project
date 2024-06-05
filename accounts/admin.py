from django.contrib import admin
from .models import (
    User, Car, Driver,
    DriverCar, City, 
    Travel, BasePrice, 
    Wallet, TransectionRequest, 
    TransectionLog,
    BasePercent,
    )
from django.contrib.auth.models import Group

admin.site.unregister(Group)
admin.site.register(User)

admin.site.register(Car)
admin.site.register(Driver)
admin.site.register(DriverCar)
admin.site.register(City)
admin.site.register(Travel)
admin.site.register(BasePrice)
admin.site.register(Wallet)
admin.site.register(TransectionRequest)
admin.site.register(TransectionLog)
admin.site.register(BasePercent)