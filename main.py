import logging
import os

from dotenv import load_dotenv
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


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    '''Send a message when the command /start is issued.'''
    await update.message.reply_text('Здравствуйте')


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    '''Echo the user message.'''
    await update.message.reply_text(update.message.text)


def main() -> None:
    '''Start the bot.'''
    load_dotenv()
    tg_token = os.getenv('TG_BOT_TOKEN')
    application = Application.builder().token(tg_token).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, echo)
    )
    application.run_polling()


if __name__ == '__main__':
    main()
