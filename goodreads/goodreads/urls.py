from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from .views import landing_page, home


urlpatterns = [
    path('', landing_page, name='landing_page'),
    path('home/', home, name='home_page'),
    path('users/', include('users.urls')),
    path('books/', include('books.urls')),
    path('api/', include('api.urls')),
    
    
    path('api-auth/', include('rest_framework.urls')),
    path('admin/', admin.site.urls),
]

# Linking static files on the project
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)