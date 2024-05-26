import requests


def get(url, params={}, timeout=5, max_retries=5, backoff_factor=0.3):
    """
    Выполнить GET-запрос
    """
    import time
    from requests.exceptions import RequestException

    retries = 0
    while retries < max_retries:
        try:
            response = requests.get(url, params=params, timeout=timeout)
            response.raise_for_status()
            return response
        except RequestException as e:
            retries += 1
            time.sleep(backoff_factor * (2 ** retries))
            if retries == max_retries:
                raise e


def get_friends(user_id, fields):
    """
    Возвращает список ID пользователей или детальную информацию о друзьях пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert isinstance(fields, str), "fields must be string"
    assert user_id > 0, "user_id must be positive integer"

    domain = "https://api.vk.com/method"
    access_token = 'vk1.a.ct-nUBTJA6TK9DL7N9g4eMEZP3ODwGg5w10KsFRcJ0VJDtqRkCnXIfM1UetK7Iped2FmaCM9piobEYoYyGDhPad9NSuGTPSJ5BIRe6C8qK6rwyCQZ-xLfUJGTw5QsJzA1lDzvZ-PgIsKHLnQpScliOkWgNcGAtAd-PQR757EsZMkZZVPEe4gy5dFRCu7RHKYFX4dTZ0VQuqEVHkN7st1gw'
    version = '5.131'  # Используем актуальную версию API

    query_params = {
        'access_token': access_token,
        'user_id': user_id,
        'fields': fields,
        'v': version
    }

    query = f"{domain}/friends.get"

    response = requests.get(query, params=query_params)
    response_data = response.json()

    if 'response' in response_data:
        return response_data['response']['items']
    else:
        raise Exception("Error fetching friends data: {}".format(
            response_data.get('error')))


def age_predict(user_id):
    """
    Прогнозирование возраста пользователя по возрасту его друзей
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"

    friends = get_friends(user_id, 'bdate')

    ages = []
    invalid_birth_dates = []
    for friend in friends:
        bdate = friend.get('bdate')
        # Если дата рождения полная (день.месяц.год)
        if bdate and len(bdate.split('.')) == 3:
            day, month, year = map(int, bdate.split('.'))
            age = 2024 - year  # Предполагаем, что текущий год - 2024
            ages.append(age)
        else:
            invalid_birth_dates.append(bdate)

    if not ages:
        print(
            f"No valid birth dates found among friends. Invalid dates: {invalid_birth_dates}")
        raise ValueError("No valid birth dates found among friends")

    predicted_age = sum(ages) / len(ages)
    return predicted_age


if __name__ == "__main__":
    user_id = 483297221
    try:
        predicted_age = age_predict(user_id)
        print(f"Predicted age for user {user_id} is {predicted_age:.2f}")
    except Exception as e:
        print(f"An error occurred: {e}")
