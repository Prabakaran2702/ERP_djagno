from django.shortcuts import get_object_or_404, render,redirect
from django.db import connection
from datetime import datetime
from django.http import JsonResponse
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView, View, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import ProductMaster,Category

# Create your views here.
class ListProduct(LoginRequiredMixin,ListView):
    model = ProductMaster
    template_name = 'product_list.html'
    context_object_name = 'products' 

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add additional context data here if needed
        return context
    
class CreateProduct(LoginRequiredMixin, CreateView):
    model = ProductMaster
    fields = ['name', 'quantity', 'desc','price','published_date','category']
    template_name = 'add_product.html'
    success_url = reverse_lazy('product_master:list_view')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.all()  # Example: Fetch all categories
        return context
    
    def post(self, request):
        # Process form data
        name = request.POST.get('name')
        quantity = request.POST.get('quantity')
        description = request.POST.get('description')
        amount = request.POST.get('amount')
        created_date = request.POST.get('created_date')
        category_id=request.POST.get('category_id')
        
         # Get the Category instance
        category = get_object_or_404(Category, id=category_id)

        # Create ProductMaster instance
        product = ProductMaster.objects.create(
            name=name,
            quantity=quantity,
            desc=description,
            price=amount,
            published_date=created_date,
            category= category
        ).save()

        # Redirect to success URL or handle as needed
        return redirect(self.success_url)
    
class DetailProduct(LoginRequiredMixin,DetailView):
    model = ProductMaster
    template_name = 'product_list.html'  
    context_object_name = 'product_detail_view'

    def get(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Handle AJAX request
            product = self.get_object()
            print(product.category,'product.category',type(product.category))

            data = {
                'id': product.id,
                'name': product.name,
                'quantity': product.quantity,
                'description': product.desc,
                'price': product.price,
                'category':product.category.Category,
                'published_date': product.published_date.strftime('%Y-%m-%d'),  # Format as needed
            }
            return JsonResponse(data)
        else:
            # Handle regular GET request
            return super().get(request, *args, **kwargs)

class UpdateProduct(LoginRequiredMixin,UpdateView):
    model = ProductMaster
    success_url = reverse_lazy('product_master:list_view')

    def post(self, request, *args, **kwargs):
        try:
            prod_id = self.kwargs.get('id')
            product = ProductMaster.objects.get(id=prod_id)
            product.name = request.POST.get('name')
            product.quantity = request.POST.get('quantity')
            product.desc = request.POST.get('desc')
            product.price = request.POST.get('price')

            published_date = request.POST.get('published_date')
            product.published_date = datetime.strptime(published_date, '%B %d, %Y').strftime('%Y-%m-%d')
            
            product.save()
            return JsonResponse({'message': 'Product updated successfully.'})
        
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})        


class DeleteProdcut(DeleteView):
    model = ProductMaster
    success_url = reverse_lazy('product_master:list_view')
    

    def post(self, request, *args, **kwargs):
        # Handle object deletion
        object_id = request.POST.get('object_id')
        object_to_delete = self.model.objects.get(id=object_id)
        object_to_delete.delete()
        return redirect(self.success_url)

    
class GenerateReport(ListView):
    model = Category
    template_name = 'report.html'
    context_object_name = 'category' 


    def post(self, request, *args, **kwargs):
        # Get the dynamic status value from the request
        category = request.POST['category_id']  # Default to 'active' if no parameter is provided
        published_date = request.POST['created_date']
        # SQL query to create or replace the view
      
        create_view_sql = """
                CREATE OR REPLACE VIEW filter_product AS
                SELECT name, quantity, `desc`, price, published_date
                FROM product_master_productmaster
                WHERE published_date = %s AND category_id = %s;
            """

        # Execute the query to create or replace the view
        with connection.cursor() as cursor:
            cursor.execute(create_view_sql, [published_date,category])

        # SQL query to fetch data from the view
        fetch_view_sql = "SELECT * FROM filter_product"

        # Execute the query to fetch data from the view
        with connection.cursor() as cursor:
            cursor.execute(fetch_view_sql)
            filter_product = cursor.fetchall()

        # Optional: Process the fetched data if needed
        products = [
            {'name': row[0], 'quantity': row[1], 'desc': row[2], 'price':row[3],'published_date': row[4]}
            for row in filter_product
        ]
        cat_obj = self.model.objects.all()

        # Render the data in a template or return as HTTP response
        return render(request, self.template_name, {'products': products, 'date':published_date, 'selected_cat':int(category),'category':cat_obj})


    