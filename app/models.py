from django.db import models
import datetime

class Product(models.Model):
    productid = models.AutoField(primary_key=True)
    productname= models.CharField(blank=False, max_length=75, unique=True)
    sell_price = models.DecimalField(decimal_places=2, max_digits=8)
    buy_price = models.DecimalField(decimal_places=2, max_digits=8)

    def __str__(self):
        return self.productname

class Transaction(models.Model):
    transaction_id=models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    Buy = 'Buy'
    Sell = 'Sell'
    buy_or_sell = [
        (Buy, 'Buy'),
        (Sell, 'Sell'),
    ]
    transacton_type = models.CharField(max_length=5, choices=buy_or_sell)
    amount = models.IntegerField(blank=False)
    transactiondate = models.DateField(default=datetime.date.today())
    total = models.IntegerField(auto_created=True)

    def save(self, *args, **kwargs):
        if self.transacton_type == 'Buy':
            self.total = self.amount
        elif self.transacton_type == 'Sell':
            self.total = (self.amount * -1)
        super(Transaction, self).save(*args, **kwargs)



