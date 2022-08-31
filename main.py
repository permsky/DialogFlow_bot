import logging
import os

from dotenv import load_dotenv
from google.cloud import dialogflow
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters
)


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def detect_intent_text(
    project_id: str,
    session_id: str,
    text: str,
    language_code: str
) -> str:
    '''Returns the result of detect intent with text as input.

    Using the same `session_id` between requests allows continuation
    of the conversation.'''
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={'session': session, 'query_input': query_input}
    )
    return response.query_result.fulfillment_text


async def resend_dialogflow_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:
    '''Send dialogflow messages to Telegram chat.'''
    dialogflow_message = detect_intent_text(
        project_id=context.bot_data['project_id'],
        session_id=update.message.chat_id,
        text=update.message.text,
        language_code=context.bot_data['language_code']
    )
    await update.message.reply_text(dialogflow_message)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    '''Send a message when the command /start is issued.'''
    await update.message.reply_text('Здравствуйте')


def main() -> None:
    '''Start the bot.'''
    load_dotenv()
    tg_token = os.getenv('TG_BOT_TOKEN')
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
    application.run_polling()


if __name__ == '__main__':
    main()
