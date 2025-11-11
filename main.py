import pyrobale
import json
from typing import Union
import time
import datetime
import jdatetime

def pbformat_message(message: pyrobale.Message, text: str):
    text = text.replace("$TEXT", str(message.text))
    text = text.replace("$UID", str(message.user.id))
    text = text.replace("$CHATID", str(message.chat.id))
    text = text.replace("$EPOCH", str(time.time()))
    text = text.replace("$TIME", str(time.strftime("%H:%M:%S")))
    now_g = datetime.datetime.now()
    now_j = jdatetime.datetime.now()
    text = text.replace("$DATE", str(now_g.strftime("%Y/%m/%d")))
    text = text.replace("$JDATE", str(now_j.strftime("%Y/%m/%d")))
    return text

class PyroJsonBale:
    def __init__(self, file_name_or_content: Union[str, dict]) -> None:
        
        if isinstance(file_name_or_content, str):
            with open(file_name_or_content, encoding="utf-8") as f:
                self.json = json.load(f)

        else:
            self.json = file_name_or_content
        
        self.bot = pyrobale.Client(self.json.get("TOKEN"))
        self._generate_bot()
    
    def _generate_bot(self):
        for hand in self.json.get('handlers'):
            if hand.get("type") == "message":
                @self.bot.on_message()
                async def on_message(message: pyrobale.Message):
                    for fltr in hand.get("filters"):
                        if fltr == "pv" or fltr == "private":
                            if message.chat.type != "private":
                                return
                            
                        if fltr == "gp" or fltr == "group":
                            if message.chat.type != "private":
                                return
                            
                        if fltr == "ch" or fltr == "channel":
                            if message.chat.type != "private":
                                return

                        if fltr == "text":
                            if not message.text:
                                return

                        if fltr.startswith("text:"):
                            if not message.text:
                                return
                            
                            if message.text != fltr.removeprefix("text:"):
                                return
                        
                        if fltr == "digit":
                            return message.text.isdigit()
                        

                    for act in hand.get('actions'):
                        if act.get("type") == "reply":
                            await message.reply(pbformat_message(message, act.get("text")))
                        
                        if act.get("type") == "answer":
                            await message.chat.send_message(pbformat_message(message, act.get("text")))

    def run(self):
        self.bot.run()


if __name__ == "__main__":
    bot = PyroJsonBale("main.pyro")
    bot.run()