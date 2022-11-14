from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls', namespace='api')),
    path('api/', include('users.urls', namespace='users')),
]

# handler404 = 'core.views.page_not_found'
# handler500 = 'core.views.server_error'
# handler403 = 'core.views.permission_denied'

if settings.DEBUG:
    # import debug_toolbar

    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
    # urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)