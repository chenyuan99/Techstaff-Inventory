from django.urls import path, include
from django.views.generic.base import RedirectView
from django.contrib import admin
from django.urls import include, re_path
from django.conf.urls import url

admin.autodiscover()

import hello.views

# To add a new path, first import the app:
# import blog
#
# Then add the new path:
# path('blog/', blog.urls, name="blog")
#
# Learn more here: https://docs.djangoproject.com/en/2.1/topics/http/urls/

app_name = 'main'  # here for namespacing of urls.
favicon_view = RedirectView.as_view(url='/static/favicon.ico', permanent=True)
urlpatterns = [
    path("", hello.views.index, name="index"),
    path("db/", hello.views.db, name="db"),
    path("admin/", admin.site.urls),
    path("register/", hello.views.register, name="register"),
    path("logout", hello.views.logout_request, name="logout"),
    path("login", hello.views.login_request, name="login"),
    path("all-building", hello.views.allbuilding, name="all-building"),
    path("jobs/", hello.views.newmanlibrary, name="jobs"),
    path("togresson-hall", hello.views.togressonhall, name="togresson-hall"),
    path("mcbryde-hall", hello.views.mcbrydehall, name="mcbryde-hall"),
    re_path(r'^favicon\.ico$', favicon_view),
    path("about", hello.views.about, name="about"),
    path("faq", hello.views.faq, name="faq"),
    path("privacy-policy", hello.views.privacy, name="privacy-policy"),
    path("check-in", hello.views.event, name="check-in"),
    path("check-out", hello.views.check_out, name="check-out"),
    path("add-guest", hello.views.add_guest, name="add-guest"),
    path("account", hello.views.account, name="account"),
    url(r'^display_laptops$', hello.views.display_laptops, name='display_laptops'),
    url(r'^display_desktops$', hello.views.display_desktops, name='display_desktops'),
    url(r'^display_mobiles$', hello.views.display_mobiles, name='display_mobiles'),

    url(r'^add_laptop$', hello.views.add_laptop, name='add_laptop'),
    url(r'^add_desktop$', hello.views.add_desktop, name='add_desktop'),
    url(r'^add_mobile$', hello.views.add_mobile, name='add_mobile'),

    url(r'^edit_laptop/(?P<pk>\d+)$', hello.views.edit_laptop, name='edit_laptop'),
    url(r'^edit_desktop/(?P<pk>\d+)$', hello.views.edit_desktop, name='edit_desktop'),
    url(r'^edit_mobile/(?P<pk>\d+)$', hello.views.edit_mobile, name='edit_mobile'),

    url(r'^delete_laptop/(?P<pk>\d+)$', hello.views.delete_laptop, name='delete_laptop'),
    url(r'^delete_desktop/(?P<pk>\d+)$', hello.views.delete_desktop, name='delete_desktop'),
    url(r'^delete_mobile/(?P<pk>\d+)$', hello.views.delete_mobile, name='delete_mobile'),
]
