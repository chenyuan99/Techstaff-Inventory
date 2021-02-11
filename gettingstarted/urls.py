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
    # re_path(r'^favicon\.ico$', favicon_view),
    path("about", hello.views.about, name="about"),
    path("faq", hello.views.faq, name="faq"),
    path("privacy-policy", hello.views.privacy, name="privacy-policy"),
    path("check-in", hello.views.ticket, name="check-in"),
    path("check-out", hello.views.check_out, name="check-out"),
    path("add-guest", hello.views.add_guest, name="add-guest"),
    path("account", hello.views.account, name="account"),
    url(r'^display_devices$', hello.views.display_devices, name='display_devices'),
    url(r'^display_hostnames$', hello.views.display_hostnames, name='display_hostnames'),
    url(r'^display_tickets$', hello.views.display_tickets, name='display_tickets'),
    url(r'^add_device$', hello.views.add_device, name='add_device'),
    url(r'^add_hostname$', hello.views.add_hostname, name='add_hostname'),
    url(r'^edit_device/(?P<pk>\d+)$', hello.views.edit_device, name='edit_device'),
    url(r'^delete_device/(?P<pk>\d+)$', hello.views.delete_device, name='delete_device'),
    url(r'^some_view$', hello.views.some_view, name='some_view'),
]
