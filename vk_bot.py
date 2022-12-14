import logging
import os
import random
import time

import vk_api as vk
from dotenv import load_dotenv
from telegram.ext import Application
from vk_api.longpoll import VkLongPoll, VkEventType, Event
from vk_api.vk_api import VkApiMethod

from dialogflow_utils import detect_intent_text
from tg_logger import TelegramLogsHandler


logger = logging.getLogger('Logger')


def resend_dialogflow_message(
    event: Event,
    vk_api: VkApiMethod,
    project_id: str,
    language_code: str
) -> None:
    '''Send dialogflow message to VK chat.'''
    dialogflow_response = detect_intent_text(
        project_id=project_id,
        session_id=event.user_id,
        text=event.text,
        language_code=language_code
    )
    if not dialogflow_response.query_result.intent.is_fallback:
        vk_api.messages.send(
            user_id=event.user_id,
            message=dialogflow_response.query_result.fulfillment_text,
            random_id=random.randint(1, 1000)
        )


def main() -> None:
    '''Start VK-bot.'''
    load_dotenv()
    tg_token = os.getenv('TG_BOT_TOKEN')
    chat_id = os.getenv('ADMIN_CHAT_ID')
    vk_session = vk.VkApi(token=os.getenv('VK_GROUP_TOKEN'))
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT_ID')
    language_code = os.getenv('LANGUAGE_CODE')

    logger.setLevel(logging.WARNING)
    application = Application.builder().token(tg_token).build()
    logger.addHandler(TelegramLogsHandler(application.bot, chat_id))

    while True:
        try:
            longpoll = VkLongPoll(vk_session)
            vk_api = vk_session.get_api()
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    resend_dialogflow_message(
                        event=event,
                        vk_api=vk_api,
                        project_id=project_id,
                        language_code=language_code
                    )
        except Exception as exc:
            logger.exception(exc)
            time.sleep(60)


if __name__ == '__main__':
    main()
