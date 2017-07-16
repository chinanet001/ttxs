from django.db import models
from ttsx_user.models import UserInfo
from ttsx_goods.models import GoodsInfo


# Create your models here.
class OrderMain(models.Model):
    order_id = models.CharField(max_length=20)  # 20170713000000uid
    user = models.ForeignKey(UserInfo)
    order_date = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=6, decimal_places=2)
    state = models.IntegerField()


class OrderDetail(models.Model):
    order = models.ForeignKey(OrderMain)
    goods = models.ForeignKey(GoodsInfo)
    count = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)

