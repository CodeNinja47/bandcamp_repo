from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, email=None, **kwargs):
        try:
            # Try email first
            if email:
                user = User.objects.get(email=email)
            else:
                # Django admin passes username field
                user = User.objects.get(email=username)
            
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
