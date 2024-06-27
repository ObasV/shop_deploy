from django.db import models

class Product(models.Model):
  title = models.CharField(max_length=255)
  description = models.TextField()
  price = models.DecimalField(max_digits=10, decimal_places=2)
  available_quantity = models.PositiveIntegerField()

  def __str__(self):
    return self.title
  


class Order(models.Model):
#   user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
  product = models.ForeignKey(Product, on_delete=models.CASCADE, default = 2)
  quantity = models.PositiveIntegerField()
  created_at = models.DateTimeField(auto_now_add=True)
  STATUS_CHOICES = (
    ('PENDING', 'Pending'),
    ('PLACED', 'Placed'),
    ('CANCELLED', 'Cancelled'),
  )
  status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')

  def __str__(self):
    return f"Order {self.id} - ({self.product.title})"


