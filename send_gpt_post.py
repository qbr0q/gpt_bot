import requests
import logging

def send_post_request(user_id, user_message,
                      assistant_content=' ', system_content=' '):
    logging.info(f'запрос от {user_id} с текстом {user_message}')
    max_tokens = 2000
    resp = requests.post(
        'http://localhost:1234/v1/chat/completions',
        headers={"Content-Type": "application/json"},
        json={
            "messages": [
                {"role": "user", "content": user_message},
                {"role": "system", "content": system_content},
                {"role": "assistant", "content": assistant_content},
            ],
            "temperature": 1.2,
            "max_tokens": max_tokens,
        }
    )
    if resp.status_code == 200 and 'choices' in resp.json():
        return resp.json()['choices'][0]['message']['content']
    else:
        return resp.json()