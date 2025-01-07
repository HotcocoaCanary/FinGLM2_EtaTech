from zhipuai import ZhipuAI


class ChatTool:
    def __init__(self, api_key, model):
        self.api_key = api_key
        self.model = model
        self.client = ZhipuAI(api_key=api_key)
        self.messages = []

    def set_message(self, messages):
        self.messages = messages

    def get_message(self):
        return self.messages

    def send_message(self):
        response = self.client.chat.completions.create(
            model=self.model,
            stream=False,
            messages=self.messages
        )
        return response