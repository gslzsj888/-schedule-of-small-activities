from django.conf.urls import patterns,include, url
from django.contrib import admin
from django.conf import settings
from billboard import views
from django.conf.urls.static import static

urlpatterns = [
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^index/$',views.index.as_view()),
    url(r'^login/$',views.login.as_view()),
    url(r'^postactivity/$',views.postactivity.as_view()),
    url(r'^myactivity/$',views.myactivity.as_view()),
    url(r'^activity/$',views.activity.as_view()),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIAS_PATH}),
]
