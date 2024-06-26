# myapp/urls.py
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('',views.home,name='home'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('recipes/', views.recipes, name='recipes'),
    path('recipe_view/', views.recipe_view, name='recipe_view'),
    path('all_recipe_view/', views.all_recipe_view, name='all_recipe_view'),
    path('get_recipe/<int:pk>/', views.get_recipe, name='get_recipe'),
    path('get_recipe2/<int:pk>/', views.get_recipe2, name='get_recipe2'),
    path('like_recipe/<int:pk>/', views.like_recipe, name='like_recipe'),
    #notification url
    path('Notification/', views.notification, name='Notification'),
   
  ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)