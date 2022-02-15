from posts import themes
from users import add_or_remove_theme, check_user_theme
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from schedule import week, lesson_numbers, lesson_names, add_lesson, format_schedule, get_today
import json


def initial_keyboard():
    board = VkKeyboard(one_time=False)
    board.add_button(
        label="Подписаться на новости класса",
        color=VkKeyboardColor.PRIMARY,
        payload={"button": 1}
    )
    board.add_line()
    board.add_button(
        label="Добавить или обновить расписание",
        color=VkKeyboardColor.PRIMARY,
        payload={"button": 2}
    )
    board.add_line()
    board.add_button(
        label="Расписание на сегодня",
        color=VkKeyboardColor.SECONDARY,
        payload={"button": 3}
    )
    board.add_button(
        label="Расписание на неделю",
        color=VkKeyboardColor.SECONDARY,
        payload={"button": 4}
    )
    return board.get_keyboard()


def button_click(user_id, payload):
    req = json.loads(payload)
    print(payload)
    if 'button' in req:
        index = req["button"]
        if index == 1:
            return {'message': 'Выберите интересующие вас темы:', 'keyboard': keyboard_events(user_id)}
        if index == 2:
            return {'message': 'Выберите день:', 'keyboard': schedule_board_day()}
        if index == 3:
            return {'message': get_today(user_id)}
        if index == 4:
            return {'message': format_schedule(user_id)}
    elif 'finish_events' in req:
        return {'message': 'Список тем обновлён.', 'keyboard': initial_keyboard()}
    elif 'theme' in req:
        msg = add_or_remove_theme(user_id, req['theme'])
        return {'message': msg.format(req['theme']), 'keyboard': keyboard_events(user_id)}
    elif 'lesson' in req:
        add_lesson(user_id, req)
        return {
            'message': 'Добавлено: {0} {1} урок {2}. {0} - выберите номер урока:'
                .format(req['day'], req['number'], req['lesson']),
            'keyboard': schedule_board_number(req['day'])
        }
    elif 'number' in req:
        return {
            'message': '{0} {1} урок - выберите предмет:'.format(req['day'], req['number']),
            'keyboard': schedule_board_choose_lesson(req['day'], req['number'])
        }
    elif 'day' in req:
        return {
            'message': '{0} - выберите номер урока:'.format(req['day']),
            'keyboard': schedule_board_number(req['day'])
        }
    elif 'finish_schedule' in req:
        return {
            'message': 'Готово! Ваше расписание: {0}'.format(format_schedule(user_id)),
            'keyboard': initial_keyboard()
        }


def keyboard_events(user_id):
    board = VkKeyboard(one_time=False)
    board.add_button(
        label="Сохранить добавленное",
        color=VkKeyboardColor.PRIMARY,
        payload={"finish_events": True}
    )
    board.add_line()
    for i in range(len(themes)):
        board.add_button(
            label=themes[i],
            color=VkKeyboardColor.POSITIVE if check_user_theme(user_id, themes[i]) else VkKeyboardColor.NEGATIVE,
            payload={"theme": themes[i]}
        )
        if i % 2:
            board.add_line()
    return board.get_keyboard()


def schedule_board_day():
    board = VkKeyboard()
    board.add_button(
        label="Завершить работу с расписанием",
        color=VkKeyboardColor.PRIMARY,
        payload={"finish_schedule": True}
    )
    for i in range(len(week)):
        if not i % 2:
            board.add_line()
        board.add_button(
            label=week[i],
            color=VkKeyboardColor.SECONDARY,
            payload={"day": week[i]}
        )
    return board.get_keyboard()


def schedule_board_number(day):
    board = VkKeyboard()
    board.add_button(
        label="Поменять день",
        color=VkKeyboardColor.PRIMARY,
        payload={"button": 2}
    )
    for i in range(len(lesson_numbers)):
        if not i % 2:
            board.add_line()
        board.add_button(
            label=lesson_numbers[i] + ' урок',
            color=VkKeyboardColor.SECONDARY,
            payload={"day": day, "number": lesson_numbers[i]}
        )
    return board.get_keyboard()


def schedule_board_choose_lesson(day, number):
    board = VkKeyboard()
    board.add_button(
        label="Назад",
        color=VkKeyboardColor.PRIMARY,
        payload={"day": day}
    )
    for i in range(len(lesson_names)):
        if not i % 2:
            board.add_line()
        board.add_button(
            label=lesson_names[i],
            color=VkKeyboardColor.SECONDARY,
            payload={"day": day, "number": number, "lesson": lesson_names[i]}
        )
    return board.get_keyboard()
