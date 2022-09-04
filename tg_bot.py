import logging
import os
import time

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters
)

from dialogflow_utils import detect_intent_text
from tg_logger import TelegramLogsHandler


logger = logging.getLogger('Logger')


async def resend_dialogflow_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:
    '''Send dialogflow messages to Telegram chat.'''
    dialogflow_response = detect_intent_text(
        project_id=context.bot_data['project_id'],
        session_id=update.message.chat_id,
        text=update.message.text,
        language_code=context.bot_data['language_code']
    )
    await update.message.reply_text(
        dialogflow_response.query_result.fulfillment_text
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    '''Send a message when the command /start is issued.'''
    await update.message.reply_text(
        f'Здравствуйте! Вас приветствует бот-помошник. '
        f'Задавайте ваши вопросы.'
    )


def main() -> None:
    '''Start Telegram-bot.'''
    load_dotenv()
    tg_token = os.getenv('TG_BOT_TOKEN')
    chat_id = os.getenv('ADMIN_CHAT_ID')
    application = Application.builder().token(tg_token).build()
    application.bot_data['project_id'] = os.getenv('GOOGLE_CLOUD_PROJECT_ID')
    application.bot_data['language_code'] = os.getenv('LANGUAGE_CODE')
    application.add_handler(CommandHandler('start', start))
    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            resend_dialogflow_message
        )
    )

    logger.setLevel(logging.WARNING)
    logger.addHandler(TelegramLogsHandler(application.bot, chat_id))

    while True:
        try:
            application.run_polling()
        except Exception as exc:
            logger.exception(exc)
            time.sleep(60)


if __name__ == '__main__':
    main()
