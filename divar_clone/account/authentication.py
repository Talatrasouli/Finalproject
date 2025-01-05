from django.contrib.auth import get_user_model

class EmailAuthBackend:
    model_user=get_user_model()
    def authenticate(self,request,username=None,password=None):
        try:
            model_user=get_user_model()
            user=self.model_user.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except(self.model_user.DoesNotExist,self.model_user.MultipleObjectsReturned):
            return None
    def get_user(self,user_id):
        try:
            return self.model_user.objects.get(pk=user_id) 
        except self.model_user.DoesNotExist:
            return       

# class EmailAuthBackend(BaseBackend):
#     def authenticate(self, request, email=None, password=None, **kwargs):
#         User = get_user_model()  # دریافت مدل کاربر سفارشی
#         try:
#             user = User.objects.get(email=email)  # جستجو بر اساس ایمیل
#             if user.check_password(password):  # بررسی رمز عبور
#                 return user
#         except User.DoesNotExist:  # اگر کاربر وجود نداشته باشد
#             return None

#     def get_user(self, user_id):
#         User = get_user_model()  # دریافت مدل کاربر
#         try:
#             return User.objects.get(pk=user_id)  # جستجو بر اساس ID
#         except User.DoesNotExist:  # اگر کاربر وجود نداشته باشد
#             return None

