Чтобы запустить говнобота, понадобится python3.7 и скачивание либы opencv_python-4.2.0-cp37-cp37m-win_amd64 https://download.lfd.uci.edu/pythonlibs/q4hpdf1k/opencv_python-4.2.0-cp37-cp37m-win_amd64.whl
Хуйня запускается после установки либ командой pip install wheel numpy vk_api python3_anticaptcha opencv_python-4.2.0-cp37-cp37m-win_amd64.whl
Вообще не понятно, для чего  этот еблан cv добавлял
Ну суть говна в том, что оно кое-как работает. Обезьяна хотела гет запросом 
"a = requests.get('https://api.vk.com/method/messages.send?v=5.95&access_tok..{token}&message=[id{uid}|{username}] использует хеллган!&peer_id=0&random_id=0'.format(token=token, uid=(info['id']), username=(vk.users.get()[0]['first_name'])))"
Накрутить себе лс, однако я эту парашу выпилил
В итоге мы получаем медленный кусок говна. Удалил всё его подозрительное дерьмо вы можете спокойно протестировать это. Я тестировал, ущербно работает, но работает
