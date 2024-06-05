from django.contrib.auth.models import UserManager


class UserManager(UserManager):
    
    def create_user(self, email, password, username, user_type):
        if not email:
            raise ValueError('You Must Have Email!')
        if not user_type:
            raise ValueError('You Must Choice Bettwen user, driver, admin')
        
    
        user = self.model(email=self.normalize_email(email), username=username, user_type=user_type)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    
    def create_driver(self, email, password, username, user_type):
        user = self.create_user(email, password, username, user_type)
        user.save(using=self._db)
        return user
    
    
    def create_superuser(self, email, password, username, user_type):
        user = self.create_user(email, password, username, user_type)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user
    
    