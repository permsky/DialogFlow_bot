import os
import random

import vk_api as vk
from dotenv import load_dotenv
from vk_api.longpoll import VkLongPoll, VkEventType, Event
from vk_api.vk_api import VkApiMethod


def echo(event: Event, vk_api: VkApiMethod) -> None:
    vk_api.messages.send(
        user_id=event.user_id,
        message=event.text,
        random_id=random.randint(1,1000)
    )


def main() -> None:
    '''Start VK-bot.'''
    load_dotenv()
    vk_session = vk.VkApi(token=os.getenv('VK_GROUP_TOKEN'))
    longpoll = VkLongPoll(vk_session)
    vk_api = vk_session.get_api()
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            echo(event=event, vk_api=vk_api)


if __name__ == '__main__':
    main()
