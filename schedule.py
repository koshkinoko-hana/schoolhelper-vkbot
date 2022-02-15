from users import UserStatus, user_list
import datetime

week = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота']
lesson_numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
lesson_names = [
    'русский язык',
    'математика',
    'физика',
    'химия',
    'литература',
    'биология',
    'физкультура',
    'география',
    'история',
    'обществознание'
]



def format_schedule(user_id):
    user = user_list.get(user_id)
    res_string = ''
    for i in user['schedule'].keys():
        if user['schedule'][i] != {}:
            res_string += i
            for j in user['schedule'][i].keys():
                res_string += '\n' + j + ' урок ' + user['schedule'][i][j]
            res_string += '\n'
    return res_string


def get_today(user_id):
    index = datetime.datetime.today().weekday()
    if index == 6:
        return 'Сегодня воскресенье! Отдыхайте)'
    else:
        i = week[index]
        user = user_list.get(user_id)
        res_string = 'Сегодня {0}:\n'.format(i)
        if user['schedule'][i] != {}:
            for j in user['schedule'][i].keys():
                res_string += '\n' + j + ' урок ' + user['schedule'][i][j]
            res_string += '\n'
        else:
            'Свободный денёк! Отдыхайте)'
    return res_string


def parse_schedule(schedule):
    rows = schedule.split('\n')
    res = {
        'понедельник': {},
        'вторник': {},
        'среда': {},
        'четверг': {},
        'пятница': {},
        'суббота': {},
    }
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

            if words[1] != 'урок':
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

            user = user_list.get(user_id)
            user['schedule'][day].update({lesson_number: ' '.join(words[3:])})
            user_list.update({user_id: user})
            return True
    user = user_list.get(user_id)
    res = parse_schedule(schedule)
    if not res:
        return False

    user['schedule'] = {**user['schedule'], **res}
    user['status'] = UserStatus.IDLE.value
    user_list.update({user_id: user})
    return True


def add_lesson(user_id, payload):
    user = user_list.get(user_id)
    user['schedule'][payload['day']].update({payload['number']: payload['lesson']})