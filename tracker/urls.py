from django.urls import path
from tracker.views import index, deleteTransaction, registration, login_page, logout_page

urlpatterns = [
    path('', index, name="index"),
    path('registration/', registration, name="registration"),
    path('login/', login_page, name="login_page"),
    path('logout_page/', logout_page, name="logout_page"),
    path('delete-transaction/<uuid>', deleteTransaction, name="deleteTransaction"),
]