import os

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from habits.models import Habit

from .tasks import send_telegram_message


@receiver(post_save, sender=Habit)
def habit_post_save(sender, instance, created, **kwargs):
    """
    Отправляет уведомление в Telegram при создании или изменении привычки.
    """
    if settings.DEBUG:  # Отключаем отправку сообщений в DEBUG режиме
        return

    # user = instance.user
    chat_id = os.environ.get(
        "TELEGRAM_CHAT_ID"
    )  # Получаем chat_id из переменной окружения

    if chat_id is None:
        print("TELEGRAM_CHAT_ID is not set in environment variables.")
        return

    if created:
        message = f"Создана новая привычка: {instance.action} в {instance.time} в {instance.place}"
    else:
        message = f"Привычка обновлена: {instance.action} в {instance.time} в {instance.place}"

    send_telegram_message.delay(
        chat_id, message
    )  # используем Celery для отправки сообщения
