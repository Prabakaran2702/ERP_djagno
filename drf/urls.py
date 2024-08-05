from django.urls import path
from . import views

app_name = 'drf'

urlpatterns = [
    path('get_data/',views.ProductView.as_view(),name='get_data'),

    path('books/', views.BookListCreate.as_view(), name='book-list-create'),
    path('books/<int:pk>/', views.BookRetrieveUpdateDestroy.as_view(), name='book-retrieve-update-destroy'),

]