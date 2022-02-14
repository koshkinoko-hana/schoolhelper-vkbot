import vk_api
import users
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

# Создаём переменную для удобства в которой хранится наш токен от группы

token = ""

# Подключаем токен и longpoll
bh = vk_api.VkApi(token=token)
vk = bh.get_api()
res = bh.method('groups.getLongPollServer', {'group_id': 210628432})
print(res)
longpoll = VkBotLongPoll(bh, group_id=210628432)

admin_list = [199496482]

update_schedule_message = '''Давай обновим расписание. 
Пришли своё расписание в формате:
Понедельник
1 урок русский язык
2 урок математика
Вторник
1 урок физкультура
и т.д.'''


# Создадим функцию для ответа на сообщения в лс группы
def send_message(user_id, text):
    bh.method('messages.send', {'peer_id': user_id, 'random_id': 0, 'message': text})


def check_is_admin(user_id):
    return user_id in admin_list

# Слушаем longpoll(Сообщения)
for event in longpoll.listen():
    print(event)
    if event.type == VkBotEventType.WALL_POST_NEW:
        print(event.__str__())
        index = event.object.text.find('#инфо')
        if index != -1:
            event_structure = event.object.text[index:].split('#')
            if event_structure[2] not in users.themes:
                print(event_structure[2])
                users.themes.append(event_structure[2])
                print(users.themes)

    if event.type == VkBotEventType.MESSAGE_NEW:
        message = event.object.message['text'].lower()
        user_id = event.object.message['from_id']
        print(user_id)
        if not users.check_or_create_user(user_id):
            send_message(user_id, 'Привет! я бот "классный помощник". Если хочешь сохранить своё расписание, '
                                  'пришли мне слово "Расписание". Если хочешь подписаться на новости класса, '
                                  'напиши "Новости"')

        elif message == 'расписание':
            users.update_status(user_id, users.UserStatus.SCHEDULE_UPDATING)
            send_message(user_id, update_schedule_message)

        elif message == 'новости':
            users.update_status(user_id, users.UserStatus.SCHEDULE_UPDATING)
            send_message(user_id, 'Пришли мне интересующие тебя темы через запятую. Доступные темы:'
                                     ', '.join(users.themes)
                         )

        elif message == 'как дела?':
            send_message(user_id, 'Хорошо, а твои как?')

        elif message == 'отмена':
                users.update_status(user_id, users.UserStatus.IDLE)
                send_message(user_id, 'Принято')

        elif users.list.get(user_id)['status'] == users.UserStatus.SCHEDULE_UPDATING.value:
            res = users.update_schedule(user_id, message)
            if not res:
                send_message(user_id, 'Я вас не понимаю! :(')
            else:
                send_message(user_id,
                             'Принято! ваше текущее расписание: \n{0}'.format(users.format_schedule(user_id)))

        elif users.list.get(user_id)['status'] == users.UserStatus.EVENTS_UPDATING.value:
            users.update_event_types(user_id, message)
            send_message(user_id,
                         'Принято! вы подписаны на следующие темы: \n{0}'
                         .format(', '.join(users.get(user_id)['event_types'])))

        else:
            send_message(user_id, 'Я вас не понимаю! :(')


