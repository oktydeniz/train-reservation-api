
from django.urls import path
from .views import TrainCapacityView

urlpatterns = [
    path('api/reservation/', TrainCapacityView.as_view(), name="reservation"),
]
