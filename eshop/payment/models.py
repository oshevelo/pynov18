from django.db import models


class BasePayment(models.Model):
    #FK order
    #FK payment system
    # status
    # delivery_price
    # products_price
    # @property
    # def total_price
    # class PaymentSystemLog(model):
    #     query = models.TextField(blank=True)  # What Paypal sent to us initially
    #     response = models.TextField(blank=True)  # What we got back from our request
    status = models.CharField(max_length=10, blank=True)
    order = models.ForeignKey("self", on_delete=models.PROTECT, blank=True, null=True, )
    # payment_system = models.ForeignKey("self", on_delete=models.PROTECT, blank=True, null=True, )
    products_price = models.DecimalField(max_digits=9, decimal_places=2, default="0.0")
    delivery_price = models.DecimalField(max_digits=9, decimal_places=2, default="0.0")

    @property
    def total_price(self):
        return self.products_price + self.delivery_price if self.delivery_price else self.products_price


class PaymentSystemLog(models.Model):
    query = models.TextField(blank=True)  # What Paypal sent to us initially
    response = models.TextField(blank=True)  # What we got back from our request
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

