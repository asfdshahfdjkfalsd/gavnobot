import base64, json, os, random, sys, time, traceback, urllib.request, cv2, requests, vk_api
from threading import Thread
from python3_anticaptcha import ImageToTextTask, errors
from vk_api.longpoll import VkChatEventType, VkEventType, VkLongPoll
from vk_api.utils import get_random_id
spamtext = 'спам какашкой'

def captcha_handler(captcha):
    if info['captcha_key'] is None:

        class show_image(Thread):

            def __init__(self, image, title):
                Thread.__init__(self)
                self.image = image
                self.title = title

            def run(self):
                img = cv2.imread(self.image)
                cv2.imshow(self.title, img)
                cv2.waitKey(0)

        resource = urllib.request.urlopen(captcha.get_url())
        out = open('captcha.jpg', 'wb')
        out.write(resource.read())
        out.close()
        show = show_image('captcha.jpg', 'captcha!')
        show.start()
        key = input('Введите каптчу, которая появилась в отдельном окне: ').strip()
        print('Каптча решена! Закройте окно с каптчей.')
        return captcha.try_again(key)
    try:
        print('Каптча! Пробуем решить каптчу...')
        key = ImageToTextTask.ImageToTextTask(anticaptcha_key=(info['captcha_key']),
          save_format='const').captcha_handler(captcha_link=(captcha.get_url()))['solution']['text']
        print('Каптча решена!')
        return captcha.try_again(key)
    except KeyError:
        print('Не удалось решить каптчу!')


try:
    inf = open('config.json', 'r')
    inf = inf.read()
    info = json.loads(inf)
except Exception as e:
    try:
        info = {'editor': False}
    finally:
        e = None
        del e

print('\n========================================================\n                    HELLGUN\n========================================================\n')
if info['editor']:
    while True:
        start_menu = input('Если хотите перейти в режим рейда, нажмите Enter.\nА если хотите поменять страницу для рейда, напишите + ')
        if start_menu == '+':
            a = int(input('Как вы хотите авторизоваться?\n1. По токену\n\n'))
            if a == 1:
                token = input('Введите свой токен: ')
                captcha = input('Введите ключ от антикаптчи(необязательно): ')
                if captcha == '':
                    captcha = None
                d = vk_api.VkApi(token=token)
                d = d.get_api()
                try:
                    editor = open('config.json', 'w')
                    id = d.users.get()[0]['id']
                    data = {'token':str(token),  'id':id,  'editor':True,
                     'captcha_key':captcha,
                     'template_file':False}
                    data = json.dumps(data, indent=4)
                    editor.write(data)
                    print('Данные обновлены!\n')
                except Exception as e:
                    print('Ошибка:\n', traceback.format_exc())
                    try:
                        if '[5]' in str(e):
                            print('\nТокен неправильный!')
                            time.sleep(3)
                        else:
                            print('Ошибка: %s. Обратитесь с этой ошибкой к @id0 в ВК.' % e)
                    finally:
                        e = None
                        del e

        if start_menu == '':
            mode = int(input('Выберите режим\n1. Конча\n2. Жопа\n3. Поставить автоответчик на самого себя\n\n'))
            if mode == 3:

                class answering(Thread):

                    def __init__(self, list_ids, list_words, attachment, choice):
                        Thread.__init__(self)
                        self.list_ids = list_ids
                        self.list_words = list_words
                        self.attachment = attachment
                        self.choice = choice

                    def run(self):
                        if self.choice == 4:
                            print('Автоответчик запущен на тебя!\n')
                            token = info['token']
                            vk_session = vk_api.VkApi(token=token, captcha_handler=captcha_handler)
                            vk = vk_session.get_api()
                            ids = self.list_ids.split(',')
                            selfid = vk.users.get()[0]['id']
                            longpoll = VkLongPoll(vk_session)
                            for event in longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW:
                                    if str(event.user_id) in ids:
                                        if event.user_id != selfid:
                                            type = event.from_me or random.choice(['text', 'text', 'e', 'sticker'])
                                            if type == 'text':
                                                vk.messages.send(peer_id=(event.peer_id),
                                                  message=(random.choice(self.list_words)),
                                                  attachment=(self.attachment),
                                                  random_id=0,
                                                  reply_to=(event.message_id))
                                        if type == 'e':
                                            vk.messages.send(peer_id=(event.peer_id),
                                              message=(random.choice(self.list_words)),
                                              attachment=(self.attachment),
                                              random_id=0,
                                              reply_to=(event.message_id))
                                            vk.messages.send(peer_id=(event.peer_id), message='э',
                                              random_id=0)
                                    if type == 'sticker':
                                        vk.messages.send(peer_id=(event.peer_id),
                                          message=(random.choice(self.list_words)),
                                          attachment=(self.attachment),
                                          random_id=0,
                                          reply_to=(event.message_id))
                                        vk.messages.send(peer_id=(event.peer_id), sticker_id=40,
                                          random_id=0)

                        if self.choice == 2:
                            print('Автоответчик запущен на свина!\n')
                            token = base64.b64decode(info['token']).decode('utf-8')
                            vk_session = vk_api.VkApi(token=token,
                              captcha_handler=captcha_handler)
                            vk = vk_session.get_api()
                            ids = self.list_ids.split(',')
                            selfid = vk.users.get()[0]['id']
                            longpoll = VkLongPoll(vk_session)
                            for event in longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and str(event.user_id) in ids and event.user_id != selfid:
                                    event.from_me or time.sleep(2)
                                    vk.messages.setActivity(type='typing', peer_id=(event.peer_id))
                                    time.sleep(random.randint(4, 9))
                                    vk.messages.send(peer_id=(event.peer_id),
                                      message=(random.choice(self.list_words)),
                                      attachment=(self.attachment),
                                      random_id=0,
                                      reply_to=(event.message_id))
                                    vk.messages.send(peer_id=(event.peer_id), sticker_id=40,
                                      random_id=0)

                        if self.choice == 3:
                            print('Автоответчик запущен на свина!\n')
                            token = base64.b64decode(info['token']).decode('utf-8')
                            vk_session = vk_api.VkApi(token=token,
                              captcha_handler=captcha_handler)
                            vk = vk_session.get_api()
                            ids = self.list_ids.split(',')
                            selfid = vk.users.get()[0]['id']
                            longpoll = VkLongPoll(vk_session)
                            for event in longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and str(event.user_id) in ids and event.user_id != selfid:
                                    event.from_me or time.sleep(2)
                                    vk.messages.setActivity(type='typing', peer_id=(event.peer_id))
                                    time.sleep(random.randint(4, 9))
                                    vk.messages.send(peer_id=(event.peer_id),
                                      message=(random.choice(self.list_words)),
                                      attachment=(self.attachment),
                                      random_id=0,
                                      reply_to=(event.message_id))

                        if self.choice == 1:
                            print('Автоответчик запущен на свина!\n')
                            token = base64.b64decode(info['token']).decode('utf-8')
                            vk_session = vk_api.VkApi(token=token,
                              captcha_handler=captcha_handler)
                            vk = vk_session.get_api()
                            ids = list_ids.split(',')
                            selfid = vk.users.get()[0]['id']
                            longpoll = VkLongPoll(vk_session)
                            for event in longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and str(event.user_id) in ids and event.user_id != selfid:
                                    event.from_me or time.sleep(2)
                                    vk.messages.setActivity(type='typing', peer_id=(event.peer_id))
                                    time.sleep(random.randint(4, 9))
                                    vk.messages.send(peer_id=(event.peer_id),
                                      message=(random.choice(list_words)),
                                      attachment=attachment,
                                      random_id=0,
                                      reply_to=(event.message_id))
                                    vk.messages.send(peer_id=(event.peer_id), message='э', random_id=0)


                list_ids = input('Чтобы поставить автоответчик на тебя тупого, введите его или свой айди через запятую: ')
                try:
                    if not info['template_file']:
                        with open('config.json', 'w') as fh:
                            destination = input('Так как вы не вводили путь до файла, введите абсолютный путь до файла с шаблонами через строчку (например C:\\Users\\Daun\\args.txt): ')
                            try:
                                open(destination, 'r')
                            except FileNotFoundError:
                                print('Вы ввели неправильный путь до файла!')
                                continue

                            info['template_file'] = destination
                            json = json.dumps(info, indent=4)
                            fh.write(json)
                            fh.close()
                except:
                    with open('config.json', 'w') as fh:
                        destination = input('Так как вы не вводили путь до файла, введите абсолютный путь до файла с шаблонами через строчку (например C:\\Users\\Daun\\args.txt): ')
                        try:
                            open(destination, 'r')
                        except FileNotFoundError:
                            print('Вы ввели неправильный путь до файла!')
                            continue

                        info['template_file'] = destination
                        json = json.dumps(info, indent=4)
                        fh.write(json)
                        fh.close()

                try:
                    file = open(info['template_file'], 'rb').read().decode('utf-8')
                except UnicodeDecodeError:
                    file = open(info['template_file'], 'rb').read().decode('windows-1251')
                except FileNotFoundError:
                    print('Файл с шаблонами не найден! Запустите ещё раз третий пункт.')
                    info['template_file'] = False
                    f = open('config.json', 'w')
                    f.write(json.dumps(info, indent=4))
                    continue

                list_words = file.split('\n')
                attachment = input('Введите ссылку на медиафайл, например "photo459509306_457244578". Если вам не нужно прикреплять медиафайл, то пропустите, нажав enter: ')
                choice = int(input('1. Отправлять с "э"\n2. Отправлять сo стикером\n3. Просто отправлять сообщение\n4. Отправлять рандомно каждый раз: либо с "э", либо со стикером, либо ни с чем\n\n'))
                thread = answering(list_ids, list_words, attachment, choice)
                thread.run()
                continue
            mode_2 = int(input('Чем флудить\n1. Смайлами\n2. Молитвами для троллинга узбеков ебливых\n3. Сообщение из message.txt\n4. Спам фото/видео/постами\n\n'))
            mode_4 = int(input('Как вы хотите начать рейд?\n1. Написав боевой клич в беседу\n2. Ввести айди беседы и начать рейд\n\n'))
            if mode_2 == 4:
                attachment = input('Введите часть ссылки как в примере photo123_123 wall123_123: ')
                mode_3 = int(input('1. Флудить с тектом из message.txt\n2. Без текста\n\n'))
            bulls = int(input('Сколько нужно выстрелов?: '))
            if mode_4 == 2:
                chat_id = input('Введите айди беседы в которой хотите начать рейд: ')
                token = base64.b64decode(info['token']).decode('utf-8')
                vk_session = vk_api.VkApi(token=token,
                  captcha_handler=captcha_handler)
                vk = vk_session.get_api()
                if mode_2 == 4:
                    if mode_3 == 2:
                        print('Флуд свинам в беседу начался!')
                        for _ in range(bulls):
                            try:
                                vk.messages.send(attachment=attachment,
                                  chat_id=chat_id,
                                  random_id=0)
                                time.sleep(random.randint(3, 5))
                            except vk_api.exceptions.ApiError as err:
                                try:
                                    if '[7]' in str(err):
                                        print('Вы были кикнуты из беседы')
                                        time.sleep(3)
                                    if '[917]' in str(err):
                                        print('Сообщение слишком длинное')
                                        time.sleep(10)
                                        sys.exit()
                                finally:
                                    err = None
                                    del err

                            except Exception as err:
                                try:
                                    print('Ошибка: %s.\nНапишите в ВК @id0 с этой ошибкой.' % err)
                                    time.sleep(30)
                                finally:
                                    err = None
                                    del err

                        a = int(input('\nФлуд закончился!. \n1. Начать рейд снова\n2. Выйти из скрипта\n\n'))
                        if a == 1:
                            continue
                        if a == 2:
                            sys.exit()
                    if mode_3 == 1:
                        print('Флуд свинам в беседу начался!')
                        for _ in range(bulls):
                            try:
                                spamtext = input('Укажите абсолютный путь до файла (например C:\\Users\\User\\hellgun\\message.txt): ')
                                spamtext = open(spamtext, 'r')
                                text = spamtext.read()
                                vk.messages.send(attachment=attachment,
                                  chat_id=chat_id,
                                  message=text,
                                  random_id=0)
                                time.sleep(random.randint(3, 5))
                            except vk_api.exceptions.ApiError as err:
                                try:
                                    if '[7]' in str(err):
                                        print('Вы были кикнуты из беседы')
                                        break
                                    if '[917]' in str(err):
                                        print('Сообщение слишком длинное')
                                        time.sleep(10)
                                        sys.exit()
                                finally:
                                    err = None
                                    del err

                            except FileNotFoundError as err:
                                try:
                                    if '[Errno 2]' in str(err):
                                        print('\nСоздайте файл message.txt!')
                                        time.sleep(10)
                                        sys.exit()
                                finally:
                                    err = None
                                    del err

                            except Exception as err:
                                try:
                                    print('Ошибка: %s.\nНапишите в ВК @id0 с этой ошибкой.' % err)
                                    time.sleep(30)
                                finally:
                                    err = None
                                    del err

                        a = int(input('\nФлуд закончился! Выберите действие \n1. Перейти в меню рейда\n2. Выйти из скрипта\n\n'))
                        if a == 1:
                            continue
                        if a == 2:
                            sys.exit()
                if mode == 1:
                    print('Флуд свинам в беседу начался!')
                    for _ in range(bulls):
                        try:
                            if mode_2 == 1:
                                pass
                            if mode_2 == 2:
                                prayers = ['Я еблан пиздец','Отдубасьте меня в школе']
                                spamtext = random.choice(prayers)
                            if mode_2 == 3:
                                spamtext = input('Укажите абсолютный путь до файла(например C:\\Users\\User\\hellgun\\message.txt): ')
                                spamtext = open(spamtext, 'r')
                                spamtext = spamtext.read()
                            vk.messages.send(chat_id=chat_id,
                              message=spamtext,
                              random_id=(get_random_id()))
                            time.sleep(random.randint(2, 4))
                        except vk_api.exceptions.ApiError as err:
                            try:
                                if '[7]' in str(err):
                                    print('Вы были кикнуты из беседы')
                                    time.sleep(3)
                                if '[917]' in str(err):
                                    print('Сообщение слишком длинное')
                                    time.sleep(10)
                                    sys.exit()
                            finally:
                                err = None
                                del err

                        except FileNotFoundError as err:
                            try:
                                if '[Errno 2]' in str(err):
                                    print('\nСоздайте файл message.txt!')
                                    time.sleep(10)
                                    sys.exit()
                            finally:
                                err = None
                                del err

                        except Exception as err:
                            try:
                                print('Ошибка: %s.\nНапишите в ВК @id0 с этой ошибкой.' % err)
                                time.sleep(30)
                            finally:
                                err = None
                                del err

                    a = int(input('\nФлуд закончился! Выберите действие \n1. Перейти в меню рейда\n2. Выйти из скрипта\n\n'))
                    if a == 1:
                        continue
                    if a == 2:
                        sys.exit()
                if mode == 2:
                    print('Флуд свинам в беседу начался!')
                    for _ in range(bulls):
                        if mode_2 == 1:
                            pass
                        elif mode_2 == 2:
                            prayers = ['хуууууууууууууууууууууууй пиздааааааааааааааааааааааааааааааааааа']
                            spamtext = random.choice(prayers)
                        elif mode_2 == 3:
                            spamtext = input('Укажите абсолютный путь до файла(например C:\\Users\\User\\hellgun\\message.txt): ')
                            spamtext = open(spamtext, 'r')
                            spamtext = spamtext.read()
                            print('Флуд свинам в беседу начался!')
                        try:
                            msg_id = vk.messages.send(chat_id=chat_id,
                              message='хелган!',
                              random_id=(get_random_id()))
                            vk.messages.edit(peer_id=(int(chat_id) + 2000000000),
                              message=spamtext,
                              message_id=msg_id)
                            time.sleep(random.randint(3, 5))
                        except vk_api.exceptions.ApiError as err:
                            try:
                                if '[7]' in str(err):
                                    print('Вы были кикнуты из беседы')
                                    time.sleep(3)
                                if '[917]' in str(err):
                                    print('Сообщение слишком длинное')
                                    time.sleep(10)
                                    sys.exit()
                            finally:
                                err = None
                                del err

                        except FileNotFoundError as err:
                            try:
                                if '[Errno 2]' in str(err):
                                    print('\nСоздайте файл message.txt!')
                                    time.sleep(10)
                                    sys.exit()
                            finally:
                                err = None
                                del err

                        except Exception as err:
                            try:
                                print('Ошибка: %s.\nНапишите в ВК @id0 с этой ошибкой.' % traceback.format_exc())
                                time.sleep(30)
                            finally:
                                err = None
                                del err

                    a = int(input('\nФлуд закончился! Выберите действие \n1. Перейти в меню рейда\n2. Выйти из скрипта\n\n'))
                    if a == 1:
                        continue
                    if a == 2:
                        sys.exit()
            if mode_4 == 1:
                call = input('Введите боевой клич, на который будут начинать флудить бот: ')
                print('Напишите в беседу %s, чтобы начать флуд!' % call)
                token = base64.b64decode(info['token']).decode('utf-8')
                vk_session = vk_api.VkApi(token=token,
                  captcha_handler=captcha_handler)
                vk = vk_session.get_api()
                longpoll = VkLongPoll(vk_session)
                for event in longpoll.listen():
                    if event.type == VkEventType.MESSAGE_NEW:
                        message = event.text
                        if message == call:
                            print('Флуд начался! Айди чата - %s' % str(event.chat_id))
                            if mode_2 == 4:
                                if mode_3 == 2:
                                    for _ in range(bulls):
                                        try:
                                            vk.messages.send(attachment=attachment,
                                              chat_id=(event.chat_id),
                                              random_id=0)
                                            time.sleep(random.randint(3, 5))
                                        except vk_api.exceptions.ApiError as err:
                                            try:
                                                if '[7]' in str(err):
                                                    print('Вы были кикнуты из беседы')
                                                    time.sleep(3)
                                                if '[917]' in str(err):
                                                    print('Сообщение слишком длинное')
                                                    time.sleep(10)
                                                    sys.exit()
                                            finally:
                                                err = None
                                                del err

                                        except Exception as err:
                                            try:
                                                print('Ошибка: %s.\nНапишите в ВК @id0 с этой ошибкой.' % err)
                                                time.sleep(30)
                                            finally:
                                                err = None
                                                del err

                                    a = int(input('\nФлуд з��кончился!. \n1. Начать рейд снова\n2. Выйти из скрипта\n\n'))
                                    if a == 1:
                                        continue
                                    if a == 2:
                                        sys.exit()
                                if mode_3 == 1:
                                    for _ in range(bulls):
                                        try:
                                            spamtext = input('Укажите абсолютный путь до файла(например C:\\Users\\User\\hellgun\\message.txt): ')
                                            spamtext = open(spamtext, 'r')
                                            text = spamtext.read()
                                            vk.messages.send(attachment=attachment,
                                              chat_id=(event.chat_id),
                                              message=text,
                                              random_id=0)
                                            time.sleep(random.randint(3, 5))
                                        except vk_api.exceptions.ApiError as err:
                                            try:
                                                if '[7]' in str(err):
                                                    print('Вы были кикнуты из беседы')
                                                    continue
                                                if '[917]' in str(err):
                                                    print('Сообщение слишком длинное')
                                                    time.sleep(10)
                                                    sys.exit()
                                            finally:
                                                err = None
                                                del err

                                        except FileNotFoundError as err:
                                            try:
                                                if '[Errno 2]' in str(err):
                                                    print('\nСоздайте файл message.txt!')
                                                    time.sleep(10)
                                                    sys.exit()
                                            finally:
                                                err = None
                                                del err

                                        except Exception as err:
                                            try:
                                                print('Ошибка: %s.\nНапишите в ВК @id0 с этой ошибкой.' % err)
                                                time.sleep(30)
                                            finally:
                                                err = None
                                                del err

                                    a = int(input('\nФлуд закончился! Выберите действие \n1. Перейти в меню рейда\n2. Выйти из скрипта\n\n'))
                                    if a == 1:
                                        continue
                                    if a == 2:
                                        sys.exit()
                            if mode == 1:
                                for _ in range(bulls):
                                    try:
                                        if mode_2 == 1:
                                            pass
                                        if mode_2 == 2:
                                            prayers = [
                                             'Я раб Аллаха ахухахухахухахухахухах']
                                            spamtext = random.choice(prayers)
                                        if mode_2 == 3:
                                            spamtext = input('Укажите абсолютный путь до файла(например C:\\Users\\User\\hellgun\\message.txt): ')
                                            spamtext = open(spamtext, 'r')
                                            spamtext = spamtext.read()
                                        vk.messages.send(chat_id=(event.chat_id),
                                          message=spamtext,
                                          random_id=(get_random_id()))
                                        time.sleep(random.randint(2, 4))
                                    except vk_api.exceptions.ApiError as err:
                                        try:
                                            if '[7]' in str(err):
                                                print('Вы были кикнуты из беседы')
                                                continue
                                            if '[917]' in str(err):
                                                print('Сообщение слишком длинное')
                                                time.sleep(10)
                                                sys.exit()
                                        finally:
                                            err = None
                                            del err

                                    except FileNotFoundError as err:
                                        try:
                                            if '[Errno 2]' in str(err):
                                                print('\nСоздайте файл message.txt!')
                                                time.sleep(10)
                                                sys.exit()
                                        finally:
                                            err = None
                                            del err

                                    except Exception as err:
                                        try:
                                            print('Ошибка: %s.\nНапишите в ВК @id0 с этой ошибкой.' % err)
                                            time.sleep(30)
                                        finally:
                                            err = None
                                            del err

                                a = int(input('\nФлуд закончился! Выберите действие \n1. Перейти в меню рейда\n2. Выйти из скрипта\n\n'))
                                if a == 1:
                                    break
                                if a == 2:
                                    sys.exit()
                            if mode == 2:
                                for _ in range(bulls):
                                    if mode_2 == 1:
                                        pass
                                    if mode_2 == 2:
                                        prayers = ['хуй пизда пиздахуй']
                                        spamtext = random.choice(prayers)
                                    if mode_2 == 3:
                                        spamtext = input('Укажите абсолютный путь до файла(например C:\\Users\\User\\hellgun\\message.txt): ')
                                        spamtext = open(spamtext, 'r')
                                        spamtext = spamtext.read()
                                    msg_id = vk.messages.send(chat_id=(event.chat_id),
                                      message='хелган!',
                                      random_id=(get_random_id()))
                                    vk.messages.edit(peer_id=(event.peer_id),
                                      message=spamtext,
                                      message_id=msg_id)
                                    time.sleep(random.randint(3, 5))

                                a = int(input('\nФлуд закончился! Выберите действие \n1. Перейти в меню рейда\n2. Выйти из скрипта\n\n'))
                                if a == 1:
                                    continue
                                if a == 2:
                                    sys.exit()

a = info['editor'] or int(input('Как вы хотите авторизоваться?\n1. По логину и паролю\n2. По токену\n\n'))
if a == 1:
    login = input('Введите логин от ВК: ')
    passw = input('Введите пароль от аккаунта: ')
    captcha_key = input('Введите ключ от антикаптчи(необязательно): ')
    if captcha_key == '':
        captcha_key = None
    try:
        t = requests.get('https://oauth.vk.com/token?grant_type=password&client_id=2274003&client_secret=hHbZxrka2uZ6jB1inYsH&username=%s' % str(login) + '&password=' + str(passw))
        token = t.json()['access_token']
        id = t.json()['user_id']
        edit2 = open('config.json', 'w')
        token = base64.b64encode(token.encode('utf-8')).decode('utf-8')
        data = {'token':str(token),  'id':id,  'editor':True,
         'captcha_key':captcha_key}
        data = json.dumps(data, indent=4)
        edit2.write(data)
        edit2.close
        print('Данные обновлены!\n')
    except Exception as err:
        try:
            try:
                if str(t.json()['error_description']) == 'open redirect_uri in browser [5]. Also you can use 2fa_supported param':
                    print('Отключите двухэтапную аутенфикацию!')
            except BaseException:
                print('\nПароль или логин неверны')
                time.sleep(3)

        finally:
            err = None
            del err

    if a == 2:
        token = input('Введите свой токен: ')
        captcha = input('Введите ключ от антикаптчи(необязательно): ')
        if captcha == '':
            captcha = None
        d = vk_api.VkApi(token=token)
        d = d.get_api()
        try:
            editor = open('config.json', 'w')
            id = d.users.get()[0]['id']
            token = base64.b64encode(token.encode('utf-8')).decode('utf-8')
            data = {'token':str(token),  'id':id,  'editor':True,
             'captcha_key':captcha,
             'template_file':False}
            data = json.dumps(data, indent=4)
            editor.write(data)
            print('Данные обновлены!\n')
        except Exception as e:
            try:
                if '[5]' in str(e):
                    print('\nТокен неправильный!')
                    time.sleep(3)
                else:
                    print('Ошибка: %s. Обратитесь с этой ошибкой к @id0 в ВК.' % e)
            finally:
                e = None
                del e
