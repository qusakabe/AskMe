from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index, name='index'),
    path('question/<int:id>', views.question, name='question'),
    path('ask/', views.ask, name='ask'),
    path('login/', views.login, name='login'),
    path('sigup/', views.signup, name='signup'),
    path('settings/', views.settings, name='settings'),
    path('tag/<int:id>/', views.tag, name='tag'),
    path('hot/', views.hot, name='hot'),
    path('logout/',views.logout_view,name='logout')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)