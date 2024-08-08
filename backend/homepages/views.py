from django.views.generic import TemplateView


class AboutUsView(TemplateView):
    """Представление для отображения информации о нас"""
    template_name = "homepages/about_us.html"

class DeliveryView(TemplateView):
    """Представление для отображения информации об условиях доставки"""
    template_name = "homepages/delivery.html"

class PromotionsView(TemplateView):
    """Представление для отображения информации об акциях"""
    template_name = "homepages/promotions.html"

class QualityAssuranceView(TemplateView):
    """Представление для отображения информации об гарантии качества"""
    template_name = "homepages/quality_assurance.html"
