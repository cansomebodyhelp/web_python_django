from django.db import models

# Модель для зберігання інформації про поїзди
class Train(models.Model):
    # Назва поїзда (максимальна довжина - 100 символів)
    name = models.CharField(max_length=100)
    # Тип поїзда (максимальна довжина - 50 символів)
    train_type = models.CharField(max_length=50)

    # Метод для строкового представлення об'єкта (використовується в адмінці)
    def __str__(self):
        return self.name

# Модель для зберігання інформації про станції
class Station(models.Model):
    # Назва станції (максимальна довжина - 100 символів)
    name = models.CharField(max_length=100)
    # Платформа станції (максимальна довжина - 50 символів)
    platform = models.CharField(max_length=50)

    # Метод для строкового представлення об'єкта
    def __str__(self):
        return self.name

# Модель для записів розкладу руху поїздів
class ScheduleRecord(models.Model):
    # Зв'язок з моделлю Train (при видаленні поїзда - видаляються всі пов'язані записи)
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    # Станція відправлення (зв'язок з моделлю Station)
    departure_station = models.ForeignKey(Station, related_name='departures', on_delete=models.CASCADE)
    # Станція прибуття (зв'язок з моделлю Station)
    arrival_station = models.ForeignKey(Station, related_name='arrivals', on_delete=models.CASCADE)
    # Час відправлення у форматі HH:MM (5 символів)
    departure_time = models.CharField(max_length=5)
    # Час прибуття у форматі HH:MM (5 символів)
    arrival_time = models.CharField(max_length=5)

    # Метод для строкового представлення запису розкладу
    def __str__(self):
        return f"{self.train} from {self.departure_station} to {self.arrival_station}"