import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from schedule import format_schedule, update_schedule
from keyboard import initial_keyboard, button_click
from posts import themes, update_themes
from users import UserStatus, user_list, update_status, check_or_create_user

token = ""

bh = vk_api.VkApi(token=token)
vk = bh.get_api()
res = bh.method('groups.getLongPollServer', {'group_id': })
print(res)
longpoll = VkBotLongPoll(bh, group_id=)


def send_message(user_id, additional):
    message_payload = {'peer_id': user_id, 'random_id': 0, **additional}
    bh.method('messages.send', message_payload)

for event in longpoll.listen():
    print(event)

    if event.type == VkBotEventType.MESSAGE_NEW:
        message = event.object.message['text'].lower()
        user_id = event.object.message['from_id']
        if not check_or_create_user(user_id):
            send_message(user_id, {'message': 'Привет! я бот "классный помощник". Если хочешь сохранить своё '
                                              'расписание, пришли мне слово "Расписание". '
                                              'Если хочешь подписаться на новости класса, '
                                              'напиши "Новости"',
                                   'keyboard': initial_keyboard()})

        elif 'payload' in event.object.message:
            res = button_click(user_id, event.object.message['payload'])
            print(res)
            send_message(user_id, res)

        elif message == 'расписание':
            update_status(user_id, UserStatus.SCHEDULE_UPDATING)
            send_message(user_id, {'message': ''''Давай обновим расписание. 
Пришли своё расписание в формате:
Понедельник
1 урок русский язык
2 урок математика
Вторник
1 урок физкультура
и т.д.'''})

        elif message == 'новости':
            update_status(user_id, UserStatus.THEMES_UPDATING)
            send_message(user_id, {'message': 'Пришли мне интересующие тебя темы через запятую. '
                                              'Доступные темы:' + ', '.join(themes)
                                   })

        elif message == 'как дела?':
            send_message(user_id, 'Хорошо, а твои как?')

        elif message == 'отмена':
            update_status(user_id, UserStatus.IDLE)
            send_message(user_id, 'Принято')

        elif user_list.get(user_id)['status'] == UserStatus.SCHEDULE_UPDATING.value:
            res = update_schedule(user_id, message)
            if not res:
                send_message(user_id, {'message': 'Я вас не понимаю! :('})
            else:
                send_message(user_id,
                             {'message': 'Принято! ваше текущее расписание: \n{0}'.format(format_schedule(user_id))})

        elif user_list.get(user_id)['status'] == UserStatus.THEMES_UPDATING.value:
            res = update_themes(user_id, message)
            if not res:
                send_message(user_id, {'message': 'Я вас не понимаю! :('})
            else:
                send_message(user_id,
                             {'message': 'Принято! вы подписаны на следующие темы: \n{0}'
                                         .format(', '.join(user_list.get(user_id)['themes']))})

        else:
            send_message(user_id, {'message': 'Я вас не понимаю! :('})

    if event.type == VkBotEventType.WALL_POST_NEW:
        index = event.object.text.find('#инфо')
        if index != -1:
            items = event.object.text[index:].split('#')
            if items[2] not in themes:
                themes.append(items[2])
        users_to_inform = dict((k, v) for (k, v) in user_list.items() if items[2] in v['themes'])
        id_ = event.object['id']
        owner_id_ = event.group_id
        wall_id = f'wall-{owner_id_}_{id_}'
        attachment = wall_id
        for key in users_to_inform:
            send_message(key, {'message': 'Внимание! Новый пост!', 'attachment': attachment})
