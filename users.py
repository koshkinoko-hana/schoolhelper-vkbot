from enum import Enum

user_list = {}


class UserStatus(Enum):
    IDLE = 'idle'
    SCHEDULE_UPDATING = 'schedule_updating'
    THEMES_UPDATING = 'themes_updating'


def check_or_create_user(user_id):
    if user_id in user_list:
        return True
    user = {
        'schedule': {
            'понедельник': {},
            'вторник': {},
            'среда': {},
            'четверг': {},
            'пятница': {},
            'суббота': {},
        },
        'themes': [],
        'status': UserStatus.IDLE.value
    }
    user_list.update({user_id: user})
    return False


def update_status(user_id, status):
    user = user_list.get(user_id)

    user['status'] = status.value
    user_list.update({user_id: user})


def add_or_remove_theme(user_id, theme):
    if theme in user_list[user_id]['themes']:
        user_list[user_id]['themes'].remove(theme)
        return '{0} удалена.'.format(theme)
    user_list[user_id]['themes'].append(theme)
    return '{0} добавлена.'.format(theme)


def check_user_theme(user_id, theme):
    return theme in user_list[user_id]['themes']