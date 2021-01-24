#!/usr/bin/env python3
import sys
import os
from config import CONFIG
import telegram
import datetime

class Send():
    def __init__(self):
        self.bot = telegram.Bot(token=CONFIG["bot_token"])
        self.admin_chat = CONFIG["admin_chat_id"]
    
    def sendInitial(self, msg):
        self.bot.sendMessage(chat_id=self.admin_chat, text=msg)

    def sendError(self, error):
        msg=f'{datetime.datetime.now()}\n{error}'
        try:
            self.bot.sendMessage(chat_id=self.admin_chat, text=msg)
            print(f"Send {msg}")
        except Exception as ex:
            print(f'{datetime.datetime.now()} Could not send [{error}], because of {ex}')
    
    def send(self, msg, chat_id):
        try:
            self.bot.sendMessage(chat_id=chat_id, text=msg)
        except Exception as ex:
            self.sendError(ex)

    def sendAll(self, msg, chat_ids):
        if chat_ids:
            for chat_id in chat_ids:
                self.send(msg,chat_id)

    def sendCheck(self, dbApi, lastTimestamp, timestamp):
        lastDevices = dbApi.devicesAt(lastTimestamp)
        if lastDevices:
            lastDevices=[x[0] for x in lastDevices]
        devices = dbApi.devicesAt(timestamp)
        if devices:
            devices=[x[0] for x in devices]
            for device in devices:
                if device not in lastDevices:
                    sendTo=dbApi.subscribers(device)
                    if sendTo:
                        sendTo=[x[0] for x in sendTo]
                        self.sendAll(f"{device} is back", sendTo)
