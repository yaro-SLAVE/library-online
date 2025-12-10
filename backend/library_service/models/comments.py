from django.db import models


class OrderItemComment(models.Model):
    comment = models.TextField()

    class Meta:
        verbose_name = "Причина отсутствия элемента заказа"
        verbose_name_plural = "Причины отсутствия элемента заказа"


class OrderComment(models.Model):
    comment = models.TextField()

    class Meta:
        verbose_name = "Комментарий по заказу"
        verbose_name_plural = "Комментарии по заказу"
