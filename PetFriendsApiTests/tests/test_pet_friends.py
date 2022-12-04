import os
from api import PetFriends
from settings import (valid_email,
                      valid_password,
                      not_valid_email,
                      not_valid_password)


pf = PetFriends()
# 1 тест учебный

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result
#2 тест учебный

def test_get_all_pets_with_valid_key(filter=""):
    """ Проверяем, что запрос списка всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее, используя этот ключ, запрашиваем список всех питомцев и
    проверяем, что список не пустой.
             Доступное значение параметра filter - pf.my_pets, pf.all_pets """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

#3 тест учебный
def test_add_new_pet_with_valid_data(name='Mushu', animal_type='кошка',
                                     age='5', pet_photo='images/cat7.jpg'):
    """ Проверяем, что запрос на добавление нового питомца с указанными параметрами выполняется успешно."""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pets(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name
#4 тест учебный
def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()

#5 тест учебный
def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


#1 для домашнего задания
def test_get_api_key_for_not_valid_email_and_password(
    email=not_valid_email,
    password=not_valid_password
):
    """ Проверяем, что запрос api ключа с неверным email пользователя
        возвращает статус 403 и в результате не содержится слово key"""
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result

#2 тест для домашнего задания
def test_add_new_pet_with_empty_age(
    name='Софочка',
    animal_type='Кошка Египетская',
    age='',
    pet_photo_path='images/cat2.jpg'
):
    """ Проверяем, что запрос на добавление нового питомца
        с пустым полем возраста выполняется успешно"""
    pet_photo_path = os.path.join(os.path.dirname(__file__), pet_photo_path)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pets(
        auth_key,
        name,
        animal_type,
        age,
        pet_photo_path
    )

    assert status == 200
    assert 'name' in result

#3 тест для домашнего задания
def test_add_new_pet_with_negative_age(
    name='Мушасик',
    animal_type='Кошка Сибирская',
    age='-6',
    pet_photo_path='images/cat7.jpg'
):
    """ Проверяем, что запрос на добавление нового питомца
        с отрицательным возрастом выполняется успешно"""
    pet_photo_path = os.path.join(os.path.dirname(__file__), pet_photo_path)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pets(
        auth_key,
        name,
        animal_type,
        age,
        pet_photo_path
    )

    assert status == 200
    assert 'name' in result

#4 тест для домашнего задания
def test_add_new_pet_with_space_in_age(
    name='Мушу',
    animal_type='Кошка Сибирская',
    age=' ',
    pet_photo_path='images/cat7.jpg'
):
    """ Проверяем, что запрос на добавление нового питомца
        с пустым полем возраста выполняется успешно"""
    pet_photo_path = os.path.join(os.path.dirname(__file__), pet_photo_path)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pets(auth_key, name, animal_type, age, pet_photo_path)

    assert status == 200
    assert 'name' in result

#5 тест для домашнего задания
def test_add_new_pet_with_incorrect_age(
    name='Мушаси',
    animal_type='Кошка Сибирская',
    age='7777777777777',
    pet_photo_path='images/cat7.jpg'
):
    """ Проверяем, что запрос на добавление нового питомца
        с некорректным параметром
            возраст питомца = 7777777777777
        выполняется успешно."""
    pet_photo_path = os.path.join(os.path.dirname(__file__), pet_photo_path)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pets(
        auth_key,
        name,
        animal_type,
        age,
        pet_photo_path
    )

    assert status == 200
    assert result['name'] == name
    assert result['age'] == age


#6 тест для домашнего задания
def test_rejection_update_self_pet_info_without_name(
    name='',
    animal_type='Кошка',
    age=2
):
    """ Проверяем невозможность очистить имя питомца
        путём передачи пустого поля name """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, pf.my_pets)
    if not my_pets['pets']:
        raise Exception("There is no my pets")
    pet_id = my_pets['pets'][0]['id']

    status, result = pf.update_pet_info(
        auth_key,
        pet_id,
        name,
        animal_type,
        age
    )

    # Проверяем что статус ответа = 200 и имя питомца не стало пустым
    assert status == 200
    assert result['name']

#7 тест для домашнего задания
def test_rejection_update_self_pet_info_without_animal_type(
    name='Муся',
    animal_type='',
    age=1
):
    """ Проверяем невозможность очистить типа питомца путём
        передачи пустого поля animal_type """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, pf.my_pets)

    if not my_pets['pets']:
        raise Exception("There is no my pets")
    pet_id = my_pets['pets'][0]['id']

    status, result = pf.update_pet_info(
        auth_key,
        pet_id,
        name,
        animal_type,
        age
    )
    # Проверяем что статус ответа = 200 и тип питомца не пустой
    assert status == 200
    assert result['animal_type']

#8 тест для домашнего задания
def test_succsessful_update_self_pet_info_with_spase_name(
    name=' ',
    animal_type='Кошкин кот',
    age=1
):
    """ Проверяем возможность очистки имени питомца путём передачи пробела
        в поле name - информация перезаписывается успешно."""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, pf.my_pets)

    if not my_pets['pets']:
        raise Exception("There is no my pets")
    pet_id = my_pets['pets'][0]['id']

    status, result = pf.update_pet_info(
        auth_key,
        pet_id,
        name,
        animal_type,
        age
    )
    # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
    assert status == 200
    assert result['name'] == ' '

#9 тест для домашнего задания
def test_add_new_pet_with_valid_data_without_foto(
    name='Тростиночка',
    animal_type='Котетский',
    age='1'):
    """ Проверяем, что запрос на добавление нового питомца
        без фото с указанными параметрами выполняется успешно."""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(
        auth_key,
        name,
        animal_type,
        age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

#10 тест для домашнего задания
def test_add_new_pet_with_incorrect_data_without_foto(
    name='@#$%^&!*',
    animal_type='',
    age=''
):
    """ Проверяем, что запрос на добавление нового питомца
        без фото с некорректно указанными параметрами
            name задаётся спецсимволами,
            animal_type и age - пустые
        выполняется успешно."""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(
        auth_key,
        name,
        animal_type,
        age
    )

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


