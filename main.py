# Голосовой помощник Софья

import datetime
from commands import wiki, tell_jokes, give_cocktail, play_radio, \
    listen_command, say_message, google_search


commands = {
    'hello': ('привет', 'хай', 'здоров',),
    'name': ('соф',),
    'wiki': ('инфо', 'скажи', 'инфу', 'знать', 'сказ', 'знае'),
    'jokes': ('анекдот', 'грустно', 'шутк', 'пошут', 'весели', 'смеш'),
    'radio': ('радио',),
    'cocktail': ('коктейл', 'напит',),
    'time': ('врем', 'час',),
}


# выполнение команд
def do_command(message):
    if any(word in message for word in commands['name']):
        say_message('Да?')
        message = listen_command()
        if any(word in message for word in commands['hello']):
            say_message('привет')
        elif 'пока' in message:
            say_message('пока')
            exit()
        elif any(word in message for word in commands['jokes']):
            tell_jokes()
        elif any(word in message for word in commands['radio']):
            play_radio()
        elif any(word in message for word in commands['time']):
            time_now = datetime.datetime.now()
            say_message(f'Сейчас: {time_now.hour}:{time_now.minute}')
        elif any(word in message for word in commands['cocktail']):
            give_cocktail()
        elif any(word in message for word in commands['wiki']):
            wiki(message)
        else:
            google_search(message)


if __name__ == '__main__':
    while True:
        command = listen_command()
        do_command(command)
