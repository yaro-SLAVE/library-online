from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    library_card = models.CharField(verbose_name="Номер читательского билета", max_length=255)
    campus_id = models.CharField(verbose_name="ID кампуса", max_length=255, null=True, blank=True)
    mira_id = models.CharField(verbose_name="ID mira", max_length=255, null=True, blank=True)
    fullname = models.CharField(verbose_name="ФИО", max_length=255, null=True, blank=True)
    department = models.CharField(verbose_name="Отдел или Институт", max_length=511, null=True, blank=True)
    banned_status_our = models.BooleanField(verbose_name="Статус бана в нашей системе", default=False, blank=True, null=False)
    banned_status_external = models.BooleanField(verbose_name="Статус бана во внешней системе", default=False, blank=True, null=False)

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def __str__(self):
        return f"Profile for {self.user.username}"


class Basket(models.Model):
    created_at = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

    def __str__(self):
        return f"Basket {self.id} for User {self.user.id}"


class BasketItem(models.Model):
    book_id = models.CharField(verbose_name="ID книги", max_length=255)
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name="items")

    class Meta:
        verbose_name = "Элемент корзины"
        verbose_name_plural = "Элементы корзины"
        unique_together = ("basket", "book_id")

    def __str__(self):
        return f"Book ID {self.book_id} in Basket {self.basket.id}"
