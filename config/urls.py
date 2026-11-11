from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView

urlpatterns = [
    # ამ სავარჯიშოში view-ები არ გვაქვს, ამიტომ მთავარი გვერდი admin-ზე გადაგვყავს
    path("", RedirectView.as_view(url="/admin/")),
    path("admin/", admin.site.urls),
]
