from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from label_mgt import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('datapoints/', views.datapoints, name='datapoints'),
    path('signout/', views.signout, name='signout'),
    path('datapoints/<int:pk>/', views.label_datapoint, name='label_datapoint'),
    path('', views.index, name='index'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
