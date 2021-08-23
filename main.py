import requests
import time
import telegram
import os
from dotenv import load_dotenv
import textwrap


def run_bot(bot, chat_id, dvmn_token):
    api_url = 'https://dvmn.org/api/long_polling/'
    headers = {"Authorization" : dvmn_token}
    timestamp = time.time()

    while True:
        try:
            params = {'timestamp': timestamp}
            response = requests.get(api_url, headers=headers, params=params)
            response.raise_for_status()
            review_status = response.json()

            if review_status['status'] == 'found':
                new_attempt = review_status['new_attempts'][0]
                lesson = new_attempt['lesson_title']
                is_negative = new_attempt['is_negative']
                timestamp = review_status['last_attempt_timestamp']
                lesson_url = f'https://dvmn.org{new_attempt["lesson_url"]}'

                if is_negative:
                    negative_message = f'''
                    🔥Преподаватель проверил работу 
                    "{lesson}"


                    🥺К сожалению, есть ошибки🥺
                    Поправьте их и отправьте еще раз!


                    {lesson_url}'''
                    bot.send_message(chat_id=chat_id, text=textwrap.dedent(negative_message))
                else:
                    positive_message = f'''
                    🔥Преподаватель проверил работу
                    "{lesson}"
                    
                    
                    🚀Работа принята🚀
                    Так держать!


                    {lesson_url}'''
                    bot.send_message(chat_id=chat_id, text=textwrap.dedent(positive_message))        

            elif review_status['status'] == 'timeout':
                    timestamp = review_status['timestamp_to_request']

        except (requests.exceptions.ReadTimeout):
            pass
        except (requests.exceptions.ConnectionError):
            time.sleep(10)


def main():
    load_dotenv()
    dvmn_token = os.getenv('DEVMAN_TOKEN')
    tg_token = os.getenv('TELEGRAM_TOKEN')
    print('tg token - ',tg_token)
    chat_id = int(os.getenv('CHAT_ID'))
    print("CHAT_ID - ", chat_id)
    bot = telegram.Bot(token=tg_token)
    run_bot(bot, chat_id, dvmn_token)


if __name__ == '__main__':
    main()