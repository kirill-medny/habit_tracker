import pytest
from django.core.exceptions import ValidationError
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from habits.models import Habit


@pytest.fixture
def user(django_user_model):
    """
    Фикстура для создания пользователя.
    """
    return django_user_model.objects.create_user(
        username="testuser", password="testpassword", email="test@example.com"
    )


@pytest.fixture
def api_client():
    """
    Фикстура для создания API клиента.
    """
    from rest_framework.test import APIClient

    return APIClient()


@pytest.fixture
def authenticated_client(user, api_client):
    """
    Фикстура для создания аутентифицированного API клиента.
    """
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    return api_client


@pytest.mark.django_db
def test_habit_create(authenticated_client):
    """
    Тест для создания привычки.
    """
    data = {
        "place": "Home",
        "time": "10:00:00",
        "action": "Read a book",
        "is_pleasant": False,
        "periodicity": 1,
        "execution_time": 60,
        "is_public": True,
    }
    url = reverse("habits:habit_create")
    response = authenticated_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    assert Habit.objects.count() == 1
    habit = Habit.objects.first()
    assert habit.action == "Read a book"


@pytest.mark.django_db
def test_habit_list(authenticated_client, user):
    """
    Тест для получения списка привычек.
    """
    Habit.objects.create(
        user=user,
        place="Home",
        time="10:00:00",
        action="Read a book",
        is_pleasant=False,
        periodicity=1,
        execution_time=60,
        is_public=True,
    )
    url = reverse("habits:habit_list")
    response = authenticated_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data["results"]) == 1
    assert response.data["results"][0]["action"] == "Read a book"


@pytest.mark.django_db
def test_habit_update(authenticated_client, user):
    """
    Тест для обновления привычки.
    """
    habit = Habit.objects.create(
        user=user,
        place="Home",
        time="10:00:00",
        action="Read a book",
        is_pleasant=False,
        periodicity=1,
        execution_time=60,
        is_public=True,
    )
    data = {
        "place": "Work",
        "time": "11:00:00",
        "action": "Drink water",
        "is_pleasant": True,
        "periodicity": 2,
        "execution_time": 30,
        "is_public": False,
    }
    url = reverse("habits:habit_update", args=[habit.pk])
    response = authenticated_client.put(url, data)
    assert response.status_code == status.HTTP_200_OK
    habit.refresh_from_db()
    assert habit.place == "Work"
    assert habit.action == "Drink water"


@pytest.mark.django_db
def test_habit_delete(authenticated_client, user):
    """
    Тест для удаления привычки.
    """
    habit = Habit.objects.create(
        user=user,
        place="Home",
        time="10:00:00",
        action="Read a book",
        is_pleasant=False,
        periodicity=1,
        execution_time=60,
        is_public=True,
    )
    url = reverse("habits:habit_delete", args=[habit.pk])
    response = authenticated_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Habit.objects.count() == 0


@pytest.mark.django_db
def test_habit_public_list(authenticated_client, user):
    """
    Тест для получения списка публичных привычек.
    """
    Habit.objects.create(
        user=user,
        place="Home",
        time="10:00:00",
        action="Read a book",
        is_pleasant=False,
        periodicity=1,
        execution_time=60,
        is_public=True,
    )
    Habit.objects.create(
        user=user,
        place="Work",
        time="11:00:00",
        action="Drink water",
        is_pleasant=True,
        periodicity=2,
        execution_time=30,
        is_public=False,
    )
    url = reverse("habits:habit_public_list")
    response = authenticated_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data["results"]) == 1
    assert response.data["results"][0]["action"] == "Read a book"


@pytest.mark.django_db
def test_habit_validators(user):
    """
    Тест для валидаторов модели Habit.
    """
    with pytest.raises(
        ValidationError
    ):
        habit = Habit(  # Создаем экземпляр, но не сохраняем сразу
            user=user,
            place="Home",
            time="10:00:00",
            action="Read a book",
            is_pleasant=False,
            periodicity=1,
            execution_time=150,
            is_public=True,
        )
        habit.full_clean()  # Вызываем валидаторы
