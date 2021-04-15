from django.urls import path, include
from django.views.generic.base import RedirectView
from django.contrib import admin
from django.urls import include, re_path
from django.conf.urls import url
from django.views.generic import TemplateView
from hello.views import HomePageView, SearchResultsView
from django.contrib.staticfiles.storage import staticfiles_storage
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
#favicon_view = RedirectView.as_view(url='/static/favicon.ico', permanent=True)
urlpatterns = [
    path("", hello.views.index, name="index"),
    path("db/", hello.views.db, name="db"),
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path("admin/", admin.site.urls),
    path("register/", hello.views.register, name="register"),
    path("logout", hello.views.logout_request, name="logout"),
    path("login", hello.views.login_request, name="login"),
    path("about", hello.views.about, name="about"),
    path("faq", hello.views.faq, name="faq"),
    path("privacy-policy", hello.views.privacy, name="privacy-policy"),
    path("account", hello.views.account, name="account"),
    path('accounts/', include('django.contrib.auth.urls')),
    # path('accounts/', include('django.contrib.auth.urls')),
    path("legacy", hello.views.legacy, name="legacy"),
    url(r'^display_devices$', hello.views.display_devices, name='display_devices'),
    url(r'^display_hostnames$', hello.views.display_hostnames, name='display_hostnames'),
    url(r'^display_userDevice$', hello.views.display_userDevice, name='display_userDevice'),
    url(r'^display_buildings$', hello.views.display_buildings, name='display_buildings'),
    url(r'^display_faculty$', hello.views.display_faculty, name='display_faculty'),
    url(r'^display_ip$', hello.views.display_ip, name='display_ip'),
    url(r'^usecase$', hello.views.display_userCase, name='display_useCase'),
# 
    url(r'^add_device$', hello.views.add_device, name='add_device'),
    url(r'^add_faculty$', hello.views.add_faculty, name='add_faculty'),
    url(r'^add_hostname$', hello.views.add_hostname, name='add_hostname'),
    url(r'^add_building$', hello.views.add_building, name='add_building'),
    url(r'^add_userDevice$', hello.views.add_userDevice, name='add_userDevice'),
    url(r'^add_ip$', hello.views.add_ip, name='add_ip'),
    # edit delete device
    # url(r'^edit_device/(?P<pk>\d+)$', hello.views.edit_device, name='edit_device'),
    url(r'^edit_device/(?P<CS_Tag>[-\w]+)$', hello.views.edit_device, name='edit_device'),
    url(r'^edit_device_detail/(?P<CS_Tag>[-\w]+)$', hello.views.edit_device_inDetailPage, name='edit_device_detail'),
    url(r'^delete_device/(?P<CS_Tag>[-\w]+)$', hello.views.delete_device, name='delete_device'),
    url(r'^view_device/(?P<CS_Tag>[-\w]+)$', hello.views.view_device, name='view_device'),

    url(r'^assign_ip/(?P<CS_Tag>[-\w]+)$', hello.views.assignip_to_device, name='assign_ip'),
    url(r'^assign_ip_new_host/(?P<CS_Tag>[-\w]+)$', hello.views.assignip_new_hostname, name='assignip_new_hostname'),
    # url(r'^delete_device/(?P<pk>\d+)$', hello.views.delete_device, name='delete_device'),
    url(r'^edit_network/(?P<pk>\d+)$', hello.views.edit_network, name='edit_network'),
    url(r'^delete_network/(?P<pk>\d+)$', hello.views.delete_network, name='delete_network'),
    url(r'^edit_building/(?P<pk>[-\w]+)$', hello.views.edit_building, name='edit_building'),
    url(r'^delete_building/(?P<pk>[-\w]+)$', hello.views.delete_building, name='delete_building'),
    url(r'^edit_faculty/(?P<PID>[-\w]+)$', hello.views.edit_faculty, name='edit_faculty'),
    url(r'^delete_faculty/(?P<PID>[-\w]+)$', hello.views.delete_faculty, name='delete_faculty'),
    url(r'^edit_userDevice/(?P<pk>\d+)$', hello.views.edit_userDevice, name='edit_userDevice'),
    url(r'^delete_userDevice/(?P<pk>\d+)$', hello.views.delete_userDevice, name='delete_userDevice'),
    url(r'^edit_ip/(?P<IPID>\d+)$', hello.views.edit_ip, name='edit_ip'),
    url(r'^delete_ip/(?P<IPID>\d+)$', hello.views.delete_ip, name='delete_ip'),

    url(r'^check-out/(?P<pk>\d+)$', hello.views.check_out, name="check-out"),
    # url(r'^export_devices$', hello.views.export_devices, name='export_devices'),
    url(r'^export_devices$', hello.views.export_filter_devices, name='export_devices'),
    url(r'^import_hostnames$', hello.views.upload_hostnames, name='import_hostnames'),
    url(r'^import_buildings$', hello.views.upload_buildings, name='import_buildings'),
    url(r'^import_facultys$', hello.views.upload_facultys, name='import_facultys'),
    url(r'^import_ips$', hello.views.upload_ips, name='import_ips'),
    url(r'^import_devices$', hello.views.upload_devices, name='import_devices'),
    # Faculty
    # other url configs
    path('search/', SearchResultsView.as_view(), name='search_results'),
    # path("device/<str:pk>/", hello.views.device),
    # favicon path:
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('img/favicon.ico')))
]