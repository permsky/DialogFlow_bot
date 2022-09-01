import asyncio
import logging
import telegram

class TelegramLogsHandler(logging.Handler):

    def __init__(self, tg_bot: telegram.ext.ExtBot, chat_id: str) -> None:
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record: logging.LogRecord) -> None:
        log_entry = self.format(record)
        loop = asyncio.get_event_loop()
        coroutine = self.tg_bot.send_message(
            chat_id=self.chat_id,
            text=log_entry
        )
        loop.run_until_complete(coroutine)
