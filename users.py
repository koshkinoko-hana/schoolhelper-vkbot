from enum import Enum

list = {}

week = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота']

lesson_numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']

lesson_names = ['урок', 'занятие']

default_schedule = {
    'понедельник': {},
    'вторник': {},
    'среда': {},
    'четверг': {},
    'пятница': {},
    'суббота': {},
}

themes = ['егэ', 'праздник', 'олимпиада', 'волонтёрство', 'курсы']


class UserStatus(Enum):
    IDLE = 'idle'
    SCHEDULE_UPDATING = 'schedule_updating'
    EVENTS_UPDATING = 'events_updating'


def check_or_create_user(user_id):
    if user_id in list:
        print('user is in the list')
        return True
    user = {
        'schedule': default_schedule,
        'event_types': [],
        'status': UserStatus.IDLE.value
    }
    print('user is new')
    list.update({user_id: user})
    return False


def update_status(user_id, status):
    user = list.get(user_id)

    user['status'] = status.value
    list.update({user_id: user})


def format_schedule(user_id):
    user = list.get(user_id)
    res_string = ''
    for i in user['schedule'].keys():
        if user['schedule'][i] != {}:
            res_string += i
            for j in user['schedule'][i].keys():
                res_string += '\n' + j + ' урок ' + user['schedule'][i][j]
            res_string += '\n'
    return res_string


def parse_schedule(schedule):
    rows = schedule.split('\n')
    res = default_schedule.copy()
    for row in rows:
        row = row.strip().lower()
        if row in week:
            day = row
        else:
            words = row.split(' ')
            if words[0] not in lesson_numbers:
                return False
            else:
                lesson_number = words[0]

            if words[1] not in lesson_names:
                return False

            res[day].update({lesson_number: ' '.join(words[2:])})
    return res


def update_schedule(user_id, schedule):
    rows = schedule.split('\n')
    if len(rows) == 1:
        words = rows[0].split(' ')
        day = words[0]
        if day not in week:
            return False
        else:
            if words[1] not in lesson_numbers:
                return False
            else:
                lesson_number = words[1]

            if words[2] not in lesson_names:
                return False

            user = list.get(user_id)
            user['schedule'][day].update({lesson_number: ' '.join(words[3:])})
            print(user['schedule'])
            list.update({user_id: user})
            return True
    day = ''
    user = list.get(user_id)
    res = parse_schedule(schedule)
    if not res:
        return False

    user['schedule'] = {**user['schedule'], **res}
    print(user['schedule'])
    user['status'] = UserStatus.IDLE.value
    list.update({user_id: user})
    return True


def update_event_types(user_id, message):
    themes = message.split(',')
    for theme in themes:
        event = theme.strip()
        if event not in themes:
            return False
        list.get(user_id)['event_types'].append(event)
    return True
