from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from cars.views import (
    CarViewSet, CommentViewSet, CarListView, CarDetailView,
    CarCreateView, CarUpdateView, CarDeleteView, register
)

router = DefaultRouter()
router.register(r'cars', CarViewSet, basename='api-cars')  # Changed basename to avoid conflicts
router.register(r'cars/(?P<car_pk>\d+)/comments', CommentViewSet, basename='car-comments')

urlpatterns = [
    # Web interface URLs first
    path('', CarListView.as_view(), name='car-list'),
    path('car/new/', CarCreateView.as_view(), name='car-create'),
    path('car/<int:pk>/', CarDetailView.as_view(), name='car-detail'),
    path('car/<int:pk>/edit/', CarUpdateView.as_view(), name='car-update'),
    path('car/<int:pk>/delete/', CarDeleteView.as_view(), name='car-delete'),
    path('car/<int:pk>/comment/', CarDetailView.as_view(), name='car-comments'),
    
    # Authentication URLs
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        template_name='registration/logged_out.html',
        next_page='/'
    ), name='logout'),
    
    # Admin URL
    path('admin/', admin.site.urls),
    
    # API URLs last
    path('api/', include((router.urls, 'api'))),
    path('api-auth/', include('rest_framework.urls')),
]