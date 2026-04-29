from django.db import models
from django.contrib.auth.models import User
import uuid


# -----------------------------
# Base Model (Abstract)
# -----------------------------
class BaseModel(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# -----------------------------
# Pizza Category
# -----------------------------
class PizzaCategory(BaseModel):
    category_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.category_name


# -----------------------------
# Pizza Model
# -----------------------------
class Pizza(BaseModel):
    category = models.ForeignKey(
        PizzaCategory,
        on_delete=models.CASCADE,
        related_name="pizzas"
    )
    pizza_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='pizzas/', null=True, blank=True)

    def __str__(self):
        return f"{self.pizza_name} ({self.category.category_name})"


# -----------------------------
# Cart Model
# -----------------------------
class Cart(BaseModel):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="carts"
    )
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        if self.user:
            return f"{self.user.username}'s Cart ({'Paid' if self.is_paid else 'Pending'})"
        return f"Guest Cart ({'Paid' if self.is_paid else 'Pending'})"


# -----------------------------
# Cart Items
# -----------------------------
class CartItems(BaseModel):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="cart_items"
    )
    pizza = models.ForeignKey(
        Pizza,
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.pizza.pizza_name}"

    def get_total_price(self):
        return self.quantity * self.pizza.price