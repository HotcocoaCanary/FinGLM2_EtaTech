from zhipuai import ZhipuAI

class ChatClient:
    def __init__(self, api_key, model):
        self.model = model
        self.client = ZhipuAI(api_key=api_key)
        self.messages = [
            {
                "role": "system",
                "content": "你是一个金融学专家，回答用户的金融相关的问题。题为多轮问答，包含中英双语。在回答问题之前我会提供你一些数据，请根据这些信息回答问题"
            }
        ]

    def add_message(self, role, content):
        self.messages.append({"role": role, "content": content})

    def remove_message(self, index):
        del self.messages[index]

    def send_message(self):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            temperature=0.0,
        )
        answer = response.choices[0].message.content
        return answer

    def clear_messages(self):
        self.messages = []