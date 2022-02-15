from users import user_list

themes = ['егэ', 'праздник', 'олимпиада', 'волонтёрство', 'курсы']


def update_themes(user_id, message):
    items = message.split(',')
    for item in items:
        theme = item.strip()
        if theme not in themes:
            return False
        user_list.get(user_id)['themes'].append(theme)
    return True
