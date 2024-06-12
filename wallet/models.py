from django.db import models
from accounts.models import User 
from orders.models import Order


class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_wallet')
    balance = models.IntegerField(default=0)  
 
    def deposite(self, amount):
        self.balance += amount
        self.save()
         
    def check_credit(self, amount):
        return amount <= self.balance
   
    def withdraw(self, amount):
        self.balance -= amount
        self.save()

  
class TransectionRequest(models.Model):
    """request for addtion wallet"""
    is_accept = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now=True)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    amount = models.IntegerField() 
    
    
class TransectionLog(models.Model):
    """ bill """
    choice = (('1', 'request'),('2', 'order'))
    transection_type = models.CharField(max_length=10, choices=choice, null=True)
    log_ids = models.IntegerField(null=True)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    amount = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    
    @property
    def get_object(self):
        if self.transection_type == '1':
            obj = TransectionRequest.objects.get(id=self.log_ids)
        else:
            try:
                obj = Order.all_objects.get(id=self.log_ids)
            except Order.DoesNotExist:
                obj = None
        return obj
    

