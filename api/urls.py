from django.urls import path
from .views import BookView, AuthView, UserView
# router = routers.DefaultRouter()
# router.register('api/user', UserViewSet, 'user')
# urlpatterns = router.urls

urlpatterns = [
  path('books/', BookView.as_view(), name='books_list'),
  path('books/<int:id>', BookView.as_view(), name='delete_book'),
  path('auth/register', AuthView.as_view(), name='register'),
  path('auth/login', AuthView.as_view(), name='login'),
  path('auth/checktoken', AuthView.as_view(), name='checktoken'),
  path('users/', UserView.as_view(), name='users_list')
]




