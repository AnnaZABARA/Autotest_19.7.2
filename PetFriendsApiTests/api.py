import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

#import json

class PetFriends:
    def __init__(self):
        self.base_url = "https://petfriends.skillfactory.ru/"
        self.my_pets = "my_pets"
        self.all_pets = " "
        # self.set_photo =

    # учебный 1
    def get_api_key(self, email, password):
        """Метод делает запрос к API сервера и возвращает статус запроса и результат в формате JSON
        c уникальным ключом пользователя, найденного по указанным email и паролем"""

        headers = {
            'email': email,
            'password': password
        }
        res = requests.get(self.base_url+"api/key", headers=headers)
        status = res.status_code
        result = ""

        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    # учебный 2
    def get_list_of_pets(self, auth_key, filter):
        """Метод делает запрос к API сервера и возвращает статус запроса и результат со списком
        найденных питомцев, совпадающих с фильтром. На данный момент фильтр имеет пустое значение
        - получить список всех питомцев, либо 'my pets' - получить список моих питомцев"""

        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}

        res = requests.get(self.base_url+'api/pets', headers=headers, params=filter)

        status = res.status_code
        result = ""

        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    # учебный 3
    def add_new_pets(self, auth_key, name, animal_type, age, pet_photo):
        """Метод отправляет (постит) на сервер данные о добавляемом питомце и возвращает статус
        запроса на сервер и результат в формате JSON с данными добавленного питомца"""

        data = MultipartEncoder(
            fields = {
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url + 'api/pets', headers=headers, data=data)
        status = res.status_code
        result = ""

        try:
            result = res.json()
        except:
            result = res.text
        print(result)
        return status, result

    # учебный 4
    def delete_pet(self, auth_key, pet_id):
        """Метод отправляет на сервер запрос на удаление питомца по указанному ID и возвращает
        статус запроса и результат в формате JSON с текстом уведомления о успешном удалении.
        На сегодняшний день тут есть баг - в result приходит пустая строка, но status при этом = 200"""

        headers = {'auth_key': auth_key['key']}

        res = requests.delete(self.base_url + 'api/pets/' + pet_id, headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result
#учебный 5
    def update_pet_info(self, auth_key, pet_id, name,
                        animal_type, age):
        """Метод отправляет запрос на сервер об обновлении данных питомуа по указанному ID и
        возвращает статус запроса и result в формате JSON с обновлённыи данными питомца"""

        headers = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'age': age,
            'animal_type': animal_type
        }

        res = requests.put(self.base_url + 'api/pets/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

#1

    def add_new_pet_without_photo(self, auth_key, name, animal_type, age):
        """Метод отправляет (постит) на сервер данные о добавляемом питомце без фото и возвращает статус запроса на сервер и результат
        в формате JSON с данными добавленного питомца. Это отрабатывается POST API запрос."""

        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age,
        }
        headers = {'auth_key': auth_key['key']}

        res = requests.post(self.base_url + 'api/create_pet_simple', headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

#2

    def add_foto_of_pet(self, auth_key, pet_id, pet_photo_path):
        """Метод отправляет запрос на сервер на добавление данных питомца - фото - по указанному ID
        и возвращает статус запроса и result в формате JSON с обновлённыи данными питомца.
        Это отрабатывается POST API запрос."""

        data = MultipartEncoder(
            fields={'pet_photo': (pet_photo_path,
                                  open(pet_photo_path, 'rb'),
                                  'image/jpeg')})
        headers = {'auth_key': auth_key['key'],
                   'Content-Type': data.content_type}

        res = requests.post(self.base_url + 'api/pets/set_photo' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result



