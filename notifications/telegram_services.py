import os
import requests
from dotenv import load_dotenv
from borrow.models import Borrow


load_dotenv()


def send_borrow_created_message(instance: Borrow) -> None:
    bot_token = os.getenv("BOT_TOKEN")
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    payload = {
        "text": f"Created a new Borrow: \n\n"
        f"- Borrow ID: {instance.id},\n"
        f"- Borrow create date: {instance.borrow_date},\n"
        f"- Expected return date: {instance.expected_return_date},\n\n"
        f"- Book ID: {instance.book.id},\n"
        f"- Book title: {instance.book.title},\n"
        f"- Book author: {instance.book.author},\n\n"
        f"- User ID: {instance.user.id},\n"
        f"- User email: {instance.user.email},\n"
        f"- User first name: {instance.user.first_name},\n"
        f"- User last name: {instance.user.last_name}",
        "parse_mode": "",
        "disable_web_page_preview": False,
        "disable_notification": False,
        "reply_to_message_id": None,
        "chat_id": os.getenv("TELEGRAM_CHAT_ID"),
    }

    headers = {
        "accept": "application/json",
        "User-Agent": "Telegram Bot SDK - (https://github.com/irazasyed/telegram-bot-sdk)",
        "content-type": "application/json",
    }

    requests.post(url, json=payload, headers=headers)


def send_borrow_overdue_message(instance: Borrow) -> None:
    bot_token = os.getenv("BOT_TOKEN")
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    payload = {
        "text": f"This Borrow is overdue: \n\n"
        f"- Borrow ID: {instance.id},\n"
        f"- Borrow create date: {instance.borrow_date},\n"
        f"- Expected return date: {instance.expected_return_date},\n\n"
        f"- Actual return date: {instance.actual_return_date},\n\n"
        f"- Book ID: {instance.book.id},\n"
        f"- Book title: {instance.book.title},\n"
        f"- Book author: {instance.book.author},\n\n"
        f"- User ID: {instance.user.id},\n"
        f"- User email: {instance.user.email},\n"
        f"- User first name: {instance.user.first_name},\n"
        f"- User last name: {instance.user.last_name}",
        "parse_mode": "",
        "disable_web_page_preview": False,
        "disable_notification": False,
        "reply_to_message_id": None,
        "chat_id": os.getenv("TELEGRAM_CHAT_ID"),
    }

    headers = {
        "accept": "application/json",
        "User-Agent": "Telegram Bot SDK - (https://github.com/irazasyed/telegram-bot-sdk)",
        "content-type": "application/json",
    }

    requests.post(url, json=payload, headers=headers)


def send_borrow_not_overdue_message() -> None:
    bot_token = os.getenv("BOT_TOKEN")
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    payload = {
        "text": f"There are no overdue borrowings today.\n\n",
        "parse_mode": "",
        "disable_web_page_preview": False,
        "disable_notification": False,
        "reply_to_message_id": None,
        "chat_id": os.getenv("TELEGRAM_CHAT_ID"),
    }

    headers = {
        "accept": "application/json",
        "User-Agent": "Telegram Bot SDK - (https://github.com/irazasyed/telegram-bot-sdk)",
        "content-type": "application/json",
    }

    requests.post(url, json=payload, headers=headers)
