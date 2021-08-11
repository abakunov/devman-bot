import requests
import time
import telegram
import os

api_url = os.getenv('API_URL')
dvmn_token = os.getenv('DEVMAN_TOKEN')
tg_token = os.getenv('TELEGRAM_TOKEN')
chat_id = int(os.getenv('CHAT_ID'))
bot = telegram.Bot(token=tg_token)

headers = {"Authorization" : dvmn_token}
timestamp = time.time()


while True:
    try:
        params = {'timestamp': timestamp}
        response = requests.get(api_url, headers=headers, params=params)
        response.raise_for_status()
        response_data = response.json()

        if response_data['status'] == 'found':
            new_attempt = response_data['new_attempts'][0]
            lesson = new_attempt['lesson_title']
            is_negative = new_attempt['is_negative']
            timestamp = response_data['last_attempt_timestamp']
            lesson_url = f'https://dvmn.org{new_attempt["lesson_url"]}'

            if is_negative:
                bot.send_message(chat_id=chat_id, text=f'🔥Преподаватель проверил работу🔥 - \n"{lesson}"\n\n'
                f'🥺К сожалению, есть ошибки🥺\nПоправьте их и отправьте еще раз!\n\n'
                f'{lesson_url}')
            else:
                bot.send_message(chat_id=chat_id, text='🔥Преподаватель проверил работу🔥 - \n"{lesson}"\n\n🚀Работа принята🚀\nТак держать!\n\n'
                f'{lesson_url}')        

        elif response_data['status'] == 'timeout':
                timestamp = response_data['timestamp_to_request']

    except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError) as e:
        print(e)