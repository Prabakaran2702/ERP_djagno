from django.urls import path
from . import views

app_name = 'product_master'

urlpatterns = [
    path('',views.ListProduct.as_view(),name='list_view'),
    path('create_view/',views.CreateProduct.as_view(),name='create_view'),
    path('detail_view/<int:pk>/',views.DetailProduct.as_view(),name='detail_view'),
    path('update_view/<int:id>/',views.UpdateProduct.as_view(),name='update_view'),
    path('delete_view/<int:id>/',views.DeleteProdcut.as_view(),name='delete_view'),

    path('reports_view/',views.GenerateReport.as_view(),name='reports_view'),
]