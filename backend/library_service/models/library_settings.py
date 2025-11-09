from typing import Self
from django.db import models


class LibrarySettings(models.Model):
    lock = models.CharField(max_length=1, null=False, primary_key=True, default="X")
    max_books_per_order = models.PositiveIntegerField(verbose_name="Максимальное количество книг в заказе", default=7)
    max_books_per_reader = models.PositiveIntegerField(verbose_name="Максимальное количество книг на руках", default=15)
    max_borrow_days = models.PositiveIntegerField(verbose_name="Максимальное количество дней на выдачу", default=2)
    holidays = models.JSONField(verbose_name="Список календарных выходных", default=list)
    logo = models.FileField(verbose_name="Логотип на сервисе", null=True, blank=True)
    new_order_wait = models.FloatField(verbose_name="Срок ожидания нового заказа (в часах)", default=1)
    processing_order_wait = models.FloatField(verbose_name="Срок задержки исполнения заказа (в часах)", default=0.5)

    def save(self, *args, **kwargs):
        self.pk = "X"
        super().save(*args, **kwargs)

    async def asave(self, *args, **kwargs):
        self.pk = "X"
        return await super().asave(*args, **kwargs)

    @staticmethod
    def get_settings() -> Self:
        return LibrarySettings.objects.get_or_create(pk="X")[0]

    @staticmethod
    async def aget_settings() -> Self:
        return (await LibrarySettings.objects.aget_or_create(pk="X"))[0]

    class Meta:
        verbose_name = "Настройки библиотеки"
        verbose_name_plural = "Настройки библиотек"
