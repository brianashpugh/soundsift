from django.conf.urls import patterns, include, url
from django.contrib import admin
from soundsift_app.views import renderEntryPage, processUsername
import sys
print sys.path

urlpatterns = patterns('',
    # Example:
    # (r'^Analytics_Project/', include('Analytics_Project.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
    #soundsift.com/
    (r'^entry_page/$', 'soundsift_project.soundsift_app.views.renderEntryPage'),
    (r'^process_username$', processUsername),
    )
