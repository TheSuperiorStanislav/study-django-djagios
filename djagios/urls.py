from django.urls import path, include
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt

from data_collector.views import (
    StatusView,
    AlertListView,
    NewAlertView,
    EditAlertView,
    DeleteAlertView,
    RecordDataApiView,
)

urlpatterns = [
    path('admin', admin.site.urls),
    path('', StatusView.as_view(), name = 'home'),
    path('alerts/', AlertListView.as_view(), name = 'alerts'),
    path('alerts/new/', NewAlertView.as_view(), name = 'alert-new'),
    path('alerts/<int:pk>/edit/', EditAlertView.as_view(), name = 'alert-edit'),
    path('alerts/<int:pk>/delete/', DeleteAlertView.as_view(), name = 'alert-delete'),
    path('record/', csrf_exempt(RecordDataApiView.as_view()), name = 'record-data'),
]
