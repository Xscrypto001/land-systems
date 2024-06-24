from django.urls import path
from . import views


urlpatterns = [

      path("",views.index,name="index"),
    
      path('login/', views.login_view,name="login"),
      path('signup/', views.signup, name='signup'),
      
      path('logout/', views.logout_view, name='logout'),
      
      path('land-listings/', views.land_listings, name='land_listings'),
      path('profile/', views.profile, name='profile'),

    path('checkout/<int:listing_id>/', views.checkout, name='checkout'),
          path("about/",views.about,name="about"),
 path('add-land/', views.add_land_view, name='add_land'),
     path('add-listing/', views.add_listing_view, name='add_listing'),



]
