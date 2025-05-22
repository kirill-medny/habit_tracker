from unittest.mock import patch

import pytest

from telegram_bot.tasks import send_telegram_message


@pytest.mark.django_db
def test_send_telegram_message():
    """
    Тест для Celery задачи send_telegram_message.
    """
    with patch("telegram_bot.tasks.requests.post") as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"ok": True}

        chat_id = "123456789"
        message = "Test message"
        result = send_telegram_message(chat_id, message)

        assert result == {"ok": True}
        mock_post.assert_called_once()
