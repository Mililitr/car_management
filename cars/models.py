from django.db import models
from django.contrib.auth.models import User

class Car(models.Model):
    """
    Модель для хранения информации об автомобилях.
    
    Attributes:
        make (CharField): Марка автомобиля (например, Toyota, Ford)
        model (CharField): Модель автомобиля (например, Camry, Mustang) 
        year (IntegerField): Год выпуска автомобиля
        description (TextField): Описание автомобиля
        created_at (DateTimeField): Дата и время создания записи
        updated_at (DateTimeField): Дата и время последнего обновления
        owner (ForeignKey): Владелец автомобиля (связь с моделью User)
    """
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100) 
    year = models.IntegerField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """
        Возвращает строковое представление автомобиля.
        
        Returns:
            str: Строка вида "год марка модель"
        """
        return f"{self.year} {self.make} {self.model}"

class Comment(models.Model):
    """
    Модель для хранения комментариев к автомобилям.
    
    Attributes:
        content (TextField): Содержание комментария
        created_at (DateTimeField): Дата и время создания комментария
        car (ForeignKey): Автомобиль, к которому относится комментарий
        author (ForeignKey): Автор комментария (связь с моделью User)
    """
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """
        Возвращает строковое представление комментария.
        
        Returns:
            str: Строка вида "Comment by автор on автомобиль"
        """
        return f"Comment by {self.author} on {self.car}"

    class Meta:
        """
        Метаданные модели Comment.
        """
        ordering = ['-created_at']  # Сортировка комментариев по дате создания (новые сверху)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'