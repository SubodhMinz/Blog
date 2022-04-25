from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('passchange/', views.PassChangeView.as_view(), name='passchange'),
    path('signup/', views.userSignupView, name='signup'),
    path('accounts/login/', views.UserLoginVie, name='login'),
    path('logout/', views.userLogout, name='logout'),
    path('blogcreate/', views.BlogCreateView, name='blogcreate'),
    path('blog-detail/<int:pk>', views.BlogDetailView.as_view(), name='blog-detail'),
    path('edit-blog/<int:pk>', views.EditBlogView, name='edit-blog'),
    path('delete-blog/<int:pk>', views.BlogDeleteView, name='delete-blog'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

