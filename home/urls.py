from django.urls import path
from .import views
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns =[
    path('', views.signin, name='signing'),
    path('welcome', views.welcome, name='home'),
    path('signin', views.logout_user, name='logout_user'),
    path('generaldata', views.generaldata, name='general'),
    path('predictpage', views.predictpage, name='predict_page'),
    path('reportpdf', views.reportpdf, name='reportpdf'),
    path('uploadcvs', views.uploadcv, name='uploadcsv'),
    path('generate-pdf', views.pdf_img, name='generate-pdf')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)