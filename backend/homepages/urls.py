from django.urls import path
from .views import AboutUsView, DeliveryView, PromotionsView, QualityAssuranceView

app_name = 'homepages'

urlpatterns = [
    path('about_us/', AboutUsView.as_view(), name='about_us'),
    path('delivery/', DeliveryView.as_view(), name='delivery'),
    path('promotions/', PromotionsView.as_view(), name='promotions'),
    path('quality_assurance/', QualityAssuranceView.as_view(), name='quality_assurance'),
]
