from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
import uuid
from datetime import datetime

# Глобальні списки для зберігання даних (заміна бази даних)
trains = []  # Список для зберігання поїздів
stations = []  # Список для зберігання станцій
schedule_records = []  # Список для зберігання записів розкладу


def parse_time(time_str):
    try:
        return datetime.strptime(time_str, "%H:%M").time()
    except ValueError:
        return None


def home(request):
    """Головна сторінка - відображає розклад руху поїздів"""

    # Форматуємо список поїздів для шаблону
    formatted_trains = [{"id": str(idx), "name": train['name']} for idx, train in enumerate(trains)]

    # Форматуємо список станцій для шаблону
    formatted_stations = [{"id": str(idx), "name": station['name']} for idx, station in enumerate(stations)]

    # Форматуємо записи розкладу
    formatted_records = []
    for record in schedule_records:
        try:
            # Отримуємо пов'язані дані про поїзд та станції
            train = trains[record['train_id']]
            departure_station = stations[record['departure_station_id']]
            arrival_station = stations[record['arrival_station_id']]

            # Додаємо відформатований запис
            formatted_records.append({
                "id": record['id'],
                "train_name": train['name'],
                "departure_station_name": departure_station['name'],
                "arrival_station_name": arrival_station['name'],
                "departure_time": record['departure_time'],
                "arrival_time": record['arrival_time'],
            })
        except (IndexError, KeyError):
            continue  # Пропускаємо пошкоджені записи

    # Рендеримо шаблон з переданими даними
    return render(request, 'schedule/index.html', {
        'records': formatted_records,
        'trains': formatted_trains,
        'stations': formatted_stations
    })


@require_http_methods(["POST"])
def create_train(request):

    # Отримуємо дані з форми
    name = request.POST.get('name')
    train_type = request.POST.get('train_type')

    # Валідація вхідних даних
    if not name or not train_type:
        return HttpResponseBadRequest("Необхідно вказати назву та тип поїзда")

    # Додаємо новий поїзд
    train_id = len(trains)
    trains.append({
        'id': train_id,
        'name': name,
        'type': train_type
    })

    return JsonResponse({
        "message": "Поїзд успішно додано",
        "id": train_id
    })


@require_http_methods(["DELETE"])
def delete_train(request, train_id):
    try:
        train_id = int(train_id)
        # Перевіряємо коректність ID
        if train_id < 0 or train_id >= len(trains):
            raise ValueError

        # Видаляємо поїзд
        del trains[train_id]

        # Оновлюємо індекси решти поїздів
        for i in range(train_id, len(trains)):
            trains[i]['id'] = i

        # Видаляємо пов'язані записи розкладу
        global schedule_records
        schedule_records = [r for r in schedule_records if r['train_id'] != train_id]

        return JsonResponse({"message": "Поїзд успішно видалено"})
    except (ValueError, IndexError):
        return HttpResponseBadRequest("Невірний ID поїзда")


@require_http_methods(["POST"])
def create_station(request):

    name = request.POST.get('name')
    platform = request.POST.get('platform')

    if not name or not platform:
        return HttpResponseBadRequest("Необхідно вказати назву та платформу")

    station_id = len(stations)
    stations.append({
        'id': station_id,
        'name': name,
        'platform': platform
    })

    return JsonResponse({
        "message": "Станцію успішно додано",
        "id": station_id
    })


@require_http_methods(["DELETE"])
def delete_station(request, station_id):

    try:
        station_id = int(station_id)
        if station_id < 0 or station_id >= len(stations):
            raise ValueError

        # Видаляємо станцію
        del stations[station_id]

        # Оновлюємо індекси решти станцій
        for i in range(station_id, len(stations)):
            stations[i]['id'] = i

        # Видаляємо пов'язані записи розкладу
        global schedule_records
        schedule_records = [
            r for r in schedule_records
            if r['departure_station_id'] != station_id
               and r['arrival_station_id'] != station_id
        ]

        return JsonResponse({"message": "Станцію успішно видалено"})
    except (ValueError, IndexError):
        return HttpResponseBadRequest("Невірний ID станції")


@require_http_methods(["POST"])
def create_record(request):

    try:
        # Отримуємо та перевіряємо дані
        train_id = int(request.POST.get('train_id'))
        departure_station_id = int(request.POST.get('departure_station_id'))
        arrival_station_id = int(request.POST.get('arrival_station_id'))
        departure_time = request.POST.get('departure_time')
        arrival_time = request.POST.get('arrival_time')

        # Перевіряємо існування поїзда та станцій
        if (train_id < 0 or train_id >= len(trains) or
                departure_station_id < 0 or departure_station_id >= len(stations) or
                arrival_station_id < 0 or arrival_station_id >= len(stations)):
            raise ValueError("Невірний ID поїзда або станції")

        # Перевіряємо формат часу
        if not parse_time(departure_time) or not parse_time(arrival_time):
            raise ValueError("Невірний формат часу")

        # Генеруємо унікальний ID та додаємо запис
        record_id = str(uuid.uuid4())
        schedule_records.append({
            'id': record_id,
            'train_id': train_id,
            'departure_station_id': departure_station_id,
            'arrival_station_id': arrival_station_id,
            'departure_time': departure_time,
            'arrival_time': arrival_time
        })

        return JsonResponse({
            "message": "Запис розкладу успішно додано",
            "id": record_id
        })
    except (ValueError, TypeError) as e:
        return HttpResponseBadRequest(f"Помилка вхідних даних: {str(e)}")


@require_http_methods(["DELETE"])
def delete_record(request, record_id):

    global schedule_records
    initial_count = len(schedule_records)

    # Фільтруємо записи, залишаючи всі крім видаленого
    schedule_records = [r for r in schedule_records if r['id'] != record_id]

    if len(schedule_records) < initial_count:
        return JsonResponse({"message": "Запис успішно видалено"})
    else:
        return HttpResponseBadRequest("Запис не знайдено")


@require_http_methods(["GET"])
def get_trains(request):

    formatted_trains = [{
        "id": train['id'],
        "name": train['name'],
        "type": train['type']
    } for train in trains]

    return JsonResponse(formatted_trains, safe=False)


@require_http_methods(["GET"])
def get_stations(request):

    formatted_stations = [{
        "id": station['id'],
        "name": station['name'],
        "platform": station['platform']
    } for station in stations]

    return JsonResponse(formatted_stations, safe=False)