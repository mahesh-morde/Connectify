from django.conf import settings
from django.urls import path, re_path
from . import views
from django.conf.urls.static import static
from .views import toggle_favorite
from django.views.generic import TemplateView


urlpatterns = [
    path("",views.index, name='landing_page'),
    path("home",views.home, name='home'),
    path("reg",views.user_reg),
    path("login",views.user_login),
    path("logout",views.user_logout),
    path("add_contact",views.add_contact, name="add_contact"),
    path("edit_contact/<int:cid>", views.edit_Contact, name="edit_contact"),
    path("delete_contact/<int:cid>", views.deleteContact),
    path('toggle_favorite/<int:contact_id>/', toggle_favorite, name='toggle_favorite'),
    path("about/", views.about_page, name='about'),
    path("contrib", views.contrib, name='contrib'),
    path('paymenthandler/',views.paymenthandler, name='paymenthandler'),
    path('search/', views.search_contact, name='search_contact'),
    path("send/<cid>",views.Filter_Contact),  
]

urlpatterns += [
    re_path(r'^.*/$', TemplateView.as_view(template_name='404.html'), name='404'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

