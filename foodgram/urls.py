from django.conf import settings
from django.conf.urls import handler404, handler500
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from . import views

handler404 = 'foodgram.views.page_not_found'  # noqa
handler500 = 'foodgram.views.server_error'  # noqa

urlpatterns = [
    path('404/', views.page_not_found, name='404'),
    path('500/', views.server_error, name='500'),
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('api/v1/', include('api.urls')),
    path('about/', include('about.urls', namespace='about')),
    path('', include('recipes.urls'))
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
