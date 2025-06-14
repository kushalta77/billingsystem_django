from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from .models import Customer, Product, Bill, BillItem
from .forms import CustomerForm, ProductForm, BillForm, BillItemForm
from decimal import Decimal, InvalidOperation
import json
from django.db.models import Sum, Avg
from django.utils import timezone




def dashboard(request):
   
    context = {
        'total_customers': Customer.objects.count(),
        'total_products': Product.objects.count(),
        'total_bills': Bill.objects.count(),
        'recent_bills': Bill.objects.select_related('customer')[:5]
    }
    return render(request, 'billing/dashboard.html', context)


def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'billing/customers/list.html', {'customers': customers})

def customer_add(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer added successfully!')
            return redirect('customer_list')
    else:
        form = CustomerForm()
    return render(request, 'billing/customers/add.html', {'form': form})

def customer_edit(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer updated successfully!')
            return redirect('customer_list')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'billing/customers/edit.html', {'form': form, 'customer': customer})

def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        customer.delete()
        messages.success(request, 'Customer deleted successfully!')
        return redirect('customer_list')
    return render(request, 'billing/customers/delete.html', {'customer': customer})

def product_list(request):
    products = Product.objects.all()
    return render(request, 'billing/products/list.html', {'products': products})

def product_add(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully!')
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'billing/products/add.html', {'form': form})

def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'billing/products/edit.html', {'form': form, 'product': product})

def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('product_list')
    return render(request, 'billing/products/delete.html', {'product': product})


def bill_list(request):
    bills = Bill.objects.select_related('customer').all()
    aggregation = bills.aggregate(
        total=Sum('grand_total'),
        average=Avg('grand_total')
    )

    total = aggregation['total'] or 0
    average = aggregation['average'] or 0

    return render(request, 'billing/bills/list.html', {
        'bills': bills,
        'total': total,
        'average': average
    })



def bill_view(request, pk):
    bill = get_object_or_404(Bill, pk=pk)
    bill_items = bill.billitem_set.select_related('product').all()
    return render(request, 'billing/bills/view.html', {
        'bill': bill,
        'bill_items': bill_items
    })

def bill_print(request, pk):
   
    bill = get_object_or_404(Bill, pk=pk)
    bill_items = bill.billitem_set.select_related('product').all()
    return render(request, 'billing/bills/print.html', {
        'bill': bill,
        'bill_items': bill_items
    })

def get_product_price(request, pk):
   
    try:
        product = Product.objects.get(pk=pk)
        return JsonResponse({'price': str(product.price)})  
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)


def bill_create(request):
    if request.method == 'POST':
        try:
            customer_id = request.POST.get('customer')
            products_data_raw = request.POST.get('products_data', '[]')
            products_data = json.loads(products_data_raw)

            if not customer_id:
                raise ValueError('Please select a customer.')

            if not products_data:
                raise ValueError('Please add at least one product.')

            customer = get_object_or_404(Customer, pk=customer_id)

            
            today = timezone.localdate()

            
            bill = Bill.objects.filter(customer=customer).first()

            if not bill:
                bill = Bill.objects.create(customer=customer)

         
            for item_data in products_data:
                product_id = item_data.get('product_id')
                product = get_object_or_404(Product, pk=product_id)

                quantity = int(item_data.get('quantity', 1))
                if quantity <= 0:
                    raise ValueError('Quantity must be positive')

                price = product.price
                total = price * quantity

                bill_item, created = BillItem.objects.get_or_create(
                    bill=bill,
                    product=product,
                    defaults={'quantity': quantity, 'price': price, 'total': total}
                )

                if not created:
                   
                    bill_item.quantity += quantity
                    bill_item.total = bill_item.price * bill_item.quantity
                    bill_item.save()

            bill.calculate_totals()

            messages.success(request, f'Bill {bill.bill_number} updated successfully!')
            return redirect('bill_view', pk=bill.pk)

        except Exception as e:
            messages.error(request, str(e))

    customers = Customer.objects.all()
    products = Product.objects.all()
    return render(request, 'billing/bills/create.html', {
        'customers': customers,
        'products': products
    })
