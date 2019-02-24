from django.urls import path

from .views import PhonebookView

urlpatterns = [
    path('', PhonebookView.as_view(), name='index'),
    path('<str:slug>', PhonebookView.as_view()),
]
