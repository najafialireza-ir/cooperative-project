from django.contrib.auth.mixins import UserPassesTestMixin


class IsAdmin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_superuser
    
    
