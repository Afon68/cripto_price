from django.db import models

class Token(models.Model):  # Лучше в единственном числе
    name = models.CharField(max_length=150, unique=True, verbose_name="Название токена")
    symbol = models.CharField(max_length=10, unique=True, verbose_name="Символ")  # Например, "ETH", "BTC"
    url_token = models.URLField(default=None,blank=True, null=True, unique=True, verbose_name="url адрес")

    class Meta:
        verbose_name = "Токен"
        verbose_name_plural = "Токены"

    def __str__(self):
        return self.symbol  # Так в админке будут видны "BTC", "ETH"

class CoinPrice(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время")
    price = models.DecimalField(max_digits=15, decimal_places=6, verbose_name="Цена USD")  
    token = models.ForeignKey(Token, on_delete=models.CASCADE, related_name="prices", verbose_name="Токен")

    class Meta:
        verbose_name = "Цена токена"
        verbose_name_plural = "Цены токенов"
        ordering = ["-timestamp"]  # Сортировка от новых к старым

    def __str__(self):
        
        return f"{self.token.symbol} = {self.price} USD"


