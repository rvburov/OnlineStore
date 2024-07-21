from django.views.generic import TemplateView


class AboutUsView(TemplateView):
    template_name = "homepages/about_us.html"

class DeliveryView(TemplateView):
    template_name = "homepages/delivery.html"

class PromotionsView(TemplateView):
    template_name = "homepages/promotions.html"

class QualityAssuranceView(TemplateView):
    template_name = "homepages/quality_assurance.html"
