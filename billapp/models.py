
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

class Customer(models.Model):
    name = models.CharField(max_length=200)
    
    phone = models.CharField(max_length=20, blank=True, null=True)
   
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - ${self.price}"
    
    class Meta:
        ordering = ['name']

class Bill(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    bill_number = models.CharField(max_length=50, unique=True)
    bill_date = models.DateTimeField(auto_now_add=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('13.00'))  
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    
    def save(self, *args, **kwargs):
        
        if not self.bill_number:
            last_bill = Bill.objects.order_by('-id').first()
            if last_bill:
                last_number = int(last_bill.bill_number.split('-')[-1])
                self.bill_number = f"BILL-{last_number + 1:06d}"
            else:
                self.bill_number = "BILL-000001"
        
        super().save(*args, **kwargs)
    
    def calculate_totals(self):
       
        if self.pk:  
            subtotal = Decimal('0.00')
            
            for item in self.billitem_set.all():
                subtotal += item.total
            
            self.subtotal = subtotal
            self.tax_amount = (subtotal * self.tax_rate) / Decimal('100')
            self.grand_total = subtotal + self.tax_amount
            
           
            Bill.objects.filter(pk=self.pk).update(
                subtotal=self.subtotal,
                tax_amount=self.tax_amount,
                grand_total=self.grand_total
            )
    
    def __str__(self):
        return f"{self.bill_number} - {self.customer.name}"
    
    class Meta:
        ordering = ['-bill_date']

class BillItem(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    
    def save(self, *args, **kwargs):
        
        if not self.price:
            self.price = self.product.price
        
       
        self.total = Decimal(str(self.price)) * Decimal(str(self.quantity))
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.product.name} x {self.quantity}"