from django.urls import path
from . import views

app_name = 'election_results_app'

urlpatterns = [
    path('polling_unit/<int:unique_id>/', views.polling_unit_result, name='polling_unit_result'),
    path('local_government_result/', views.local_government_result, name='local_government_result'),
    path('add_polling_unit_result/', views.add_polling_unit_result, name='add_polling_unit_result'),
]