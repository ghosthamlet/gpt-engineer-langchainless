
from typing import List, Optional, Union

import time
import requests

import openai


TIMEOUT = 60.0


class Message:
    pass


class AIMessage(Message):
    def __init__(self, content):
        self.role = 'assistant'
        self.content = content


class HumanMessage(Message):
    def __init__(self, content):
        self.role = 'user'
        self.content = content


class SystemMessage(Message):
    def __init__(self, content):
        self.role = 'system'
        self.content = content


def messages_from_dict(messages):
    ret = []
    for v in messages:
        if v['role'] == 'assistant':
            cls = AIMessage
        elif v['role'] == 'user':
            cls = HumanMessage 
        elif v['role'] == 'system':
            cls = SystemMessage 
        ret.append(cls(v['content']))

    return ret    


def messages_to_dict(messages):
    ret = []
    for v in messages:
        ret.append({'role': v.role, 'content': v.content})

    return ret    


class StreamingStdOutCallbackHandler:
    pass


class BaseChatModel:
    pass


class ChatOpenAI(BaseChatModel):
    def __init__(
        self,
        model="gpt-4",
        temperature=1.0,
        streaming=True,
        client=openai.ChatCompletion,
    ):
        self.model = model
        self.temperature = temperature
        self.streaming = streaming 
        self.client = client 
    
        self.use_api_proxy = True
        self.config = {
                'gpt-3.5-turbo': {
                    'url': 'https://api.nextweb.fun/openai/v1/chat/completions',
                    'api_key': 'ak-xaEnQKnITocp8sWpT09tBsXAabq1jpkm6kQkGnwzvcXROFtW'
                    },
                }

    def __call__(self, messages: List[Message], callbacks=None):
        gpt_resp = requests.post(
            url=self.config[self.model]['url'],
            # proxies = proxies,
            headers=_build_request_headers(
                self.config[self.model]['api_key'], self.use_api_proxy), 
            json=_build_request_json(
               messages_to_dict(messages), self.streaming, self.use_api_proxy),
            timeout=TIMEOUT,
            stream=self.streaming
        )

        if self.streaming:
            def stream():
                for chunk in gpt_resp.iter_lines():
                  # print(chunk)
                  # print(chunk.decode("utf-8"))
                  # print(chunk.decode("utf-8").split("data: "))
                    if chunk == b'' or chunk == b'data: [DONE]':
                        continue
                    try:
                        decoded_line = json.loads(chunk.decode("utf-8").split("data: ")[1])
                        token = decoded_line["choices"][0]['delta'].get('content')

                        if token != None: 
                            yield token
                            
                    except GeneratorExit:
                        break

                    except Exception as e:
                        raise

                        print(e)
                        print(e.__traceback__.tb_next)
                        continue
                        
            return app.response_class(stream(), mimetype='text/event-stream')

        try:
            res_json = gpt_resp.json()
            print(res_json)

            return AIMessage(res_json['choices'][-1]['message']['content'])
        except Exception as e:
            print('Decode response failed, retry...')

            time.sleep(1.0)

            return self(messages, callbacks)


def _build_request_headers(api_key, use_api_proxy):
    if use_api_proxy:
        return {
                'Authorization': f'Bearer {api_key}' 
                }

    return {
            'api-key': api_key
            }


def _build_request_json(messages, use_stream, use_api_proxy):
    if use_api_proxy:
        return {
                "model": 'gpt-3.5-turbo-0301', # "gpt-3.5-turbo",
                "messages": messages,
                }

    return {
            # 'engine': "law",
            'temperature': 0.2,
            'max_tokens': 1000,
            # too small will cause repeat, and have facts errors
            'top_p': 0.7,
            'frequency_penalty': 0,
            'presence_penalty': 0,

            # 'model': request.json['model'], 
            'messages': conversation,
            'stream': use_stream
            }


