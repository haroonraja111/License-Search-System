from django.urls import path, re_path
from licenses import views

app_name = 'licenses'  # For namespacing

urlpatterns = [
    # Auth routes
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Search route
    path('search/', views.search_view, name='search'),

    # License detail (uses helper functions inside views)
    re_path(r'^detail/(?P<model_name>[^/]+)/(?P<pk>.+)/$', views.license_detail_view, name='license_detail'),
]
