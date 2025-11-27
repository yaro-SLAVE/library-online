from django.db import models
from django.contrib.auth import get_user_model

from library_service.models.catalog import Library

User = get_user_model()


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    library = models.ForeignKey(Library, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"Order {self.id} by User {self.user.id}"


class OrderHistory(models.Model):
    class Status(models.TextChoices):
        NEW = "new", "Новый"
        PROCESSING = "processing", "Собирается"
        READY = "ready", "Готов к выдаче"
        DONE = "done", "Выполнен"
        CANCELLED = "cancelled", "Отменен"
        ERROR = "error", "Ошибка"
        ARCHIVED = "archived", "Заархивирован"

    NOT_CAME_DESCRIPTION = 'не пришел'
    
    description = models.TextField()
    status = models.CharField(max_length=255, choices=Status.choices)
    date = models.DateTimeField(auto_now_add=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="statuses")
    staff = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = "История"
        verbose_name_plural = "Истории"

    def __str__(self):
        return f"History for Order {self.order.id}"


class OrderItem(models.Model):
    class Status(models.TextChoices):
        ORDERED = "ordered", "Заказана"
        HANDED = "handed", "Выдана"
        RETURNED = "returned", "Возвращена"
        CANCELLED = "cancelled", "Не найдена"
        ANALOGOUS = "analogous", "Подобран аналог"

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="books")
    book_id = models.CharField(max_length=255)
    status = models.CharField(max_length=255, choices=Status.choices, default=Status.ORDERED)
    description = models.CharField(max_length=255, null=True, blank=True)
    order_to_return = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    handed_date = models.DateTimeField(null=True, blank=True)
    to_return_date = models.DateTimeField(null=True, blank=True)
    returned_date = models.DateTimeField(null=True, blank=True)
    analogous_order_item = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "Элемент заказа"
        verbose_name_plural = "Элементы заказа"

    def __str__(self):
        return f"Exemplar ID {self.book_id} in Order {self.order.id}"
