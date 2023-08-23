
import openai


class Message:
    pass


class AIMessage(Message):
    def __init__(self, content):
        self.role = 'ai'
        self.content = content


class HumanMessage(Message):
    def __init__(self, content):
        self.role = 'user'
        self.content = content


class SystemMessage(Message):
    def __init__(self, content):
        self.role = 'system'
        self.content = content


class messages_from_dict:
    pass


class messages_to_dict:
    pass


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
    )
    self.model = model
    self.temperature = temperature
    self.streaming = streaming 
    self.client = client 

    def __call__(self, messages: List[Message], callbacks=None):
        pass

