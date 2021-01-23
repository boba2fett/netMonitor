from datetime import datetime
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime, Boolean, ForeignKeyConstraint
from config import CONFIG
from sqlalchemy.sql import select, exists


class DbApi():
    
    def __init__(self):
        self.engine = create_engine(CONFIG["db_connection"])
        meta = MetaData()

        self.network = Table(
        'network', meta,
        Column('timestamp', DateTime(timezone=True), primary_key=True),
        Column('ip', String, primary_key=True),
        Column('device_name', String)
        )

        self.subscribe = Table(
        'subscribe', meta,
        Column('timestamp', DateTime(timezone=True)),
        Column('chat_id', String, primary_key=True),
        Column('net_device', String, primary_key=True),
        Column('username', String),
        Column('first_name', String),
        Column('last_name', String)
        )

        self.auth = Table(
        'auth', meta,
        Column('timestamp', DateTime(timezone=True)),
        Column('chat_id', String, primary_key=True)
        )

        meta.create_all(self.engine)
        self.conn = self.engine.connect()

    def authenticate(self,chat_id):
        self.conn.execute(self.auth.insert(None).values(
                timestamp=datetime.now(),
                chat_id=chat_id
            )
        )

    def authenticated(self,chat_id):
        req = self.conn.execute(self.auth.select()
            .where(self.auth.c.chat_id==chat_id).count()
        )
        if req:
            req=list(req)
            return req[0][0]==1
        return False
    
    def dbCollect(self,data,time):
        if data:
            for device in data:
                self.conn.execute(self.network.insert(None).values(
                        timestamp=time,
                        device_name=device["device_name"],
                        ip=device["ip"]
                    )
                )

    def getlastTimestamp(self):
        dataend = self.conn.execute(select([self.network.c.timestamp]).order_by(self.network.c.timestamp.desc())).first()
        if dataend:
            dataend=dataend[0]
        return dataend
    
    def devicesAt(self, timestamp):
        return self.conn.execute(select([self.network.c.device_name]).where(self.network.c.timestamp==timestamp))

    def users(self):
        return self.conn.execute(select([self.network.c.ip, self.network.c.device_name]).distinct())

    def subscribedUsers(self):
        return self.conn.execute(select([self.subscribe.c.net_device]).distinct())

    def chatSubscribedUsers(self, chat_id):
        return self.conn.execute(select([self.subscribe.c.net_device]).where(self.subscribe.c.chat_id == chat_id ))

    def lastState(self, device_name):
        return self.conn.execute(self.network.select()
            .where(self.network.c.device_name==device_name)
            .order_by(self.network.c.timestamp.desc())
            ).first()

    def subscribers(self, device_name):
        return self.conn.execute(select([self.subscribe.c.chat_id])
            .where(self.subscribe.c.net_device==device_name)
        )

    def newSubscriber(self, chat_id,device_name, username, first_name, last_name):
        self.conn.execute(self.subscribe.insert(None)
            .values(
                timestamp=datetime.now(),
                chat_id = chat_id,
                net_device = device_name,
                username = username,
                first_name = first_name,
                last_name = last_name
            )
        )
    
    def rmSubscriber(self, chat_id, device_name):
        self.conn.execute(self.subscribe.delete(None)
            .where(self.subscribe.c.chat_id == chat_id)
            .where(self.subscribe.c.net_device == device_name)
        )

    def test(self):
        try:
            return f"Started, db seems to work\nStatus:\n"+self.adminStatus()
        except Exception as e:
            return f"Started, db doesn't seem to work: {e}"

    def adminStatus(self):
            subscribedusers = self.conn.execute(select([self.subscribe.c.net_device]).distinct().count())
            if subscribedusers:
                subscribedusers = [x[0] for x in subscribedusers]
            subscribtions = self.conn.execute(select([self.subscribe.c.net_device]).count())
            if subscribtions:
                subscribtions = [x[0] for x in subscribtions]
            datasets = self.conn.execute(select([self.network]).count())
            if datasets:
                datasets = [x[0] for x in datasets]
            databegin = self.conn.execute(select([self.network.c.timestamp]).order_by(self.network.c.timestamp)).first()
            if databegin:
                databegin=databegin[0]
            dataend = self.conn.execute(select([self.network.c.timestamp]).order_by(self.network.c.timestamp.desc())).first()
            if dataend:
                dataend=dataend[0]
            actual_subscribtions = self.conn.execute(select([self.subscribe.c.username,self.subscribe.c.net_device]))
            if actual_subscribtions:
                actual_subscribtions = "\n".join([f"{x[0]} -> {x[1]}" for x in actual_subscribtions])

            now_online = self.conn.execute(select([self.network.c.ip, self.network.c.device_name]).where(self.network.c.timestamp==dataend))
            if now_online:
                now_online = "\n".join([f"{x[0]}: {x[1]}" for x in now_online])
            return f"""
subscribtions: {subscribtions}
subscribedusers: {subscribedusers}
datasets: {datasets}
from: [{databegin}]
until: [{dataend}]

subsriptions:
{actual_subscribtions}

current:
{now_online}
"""