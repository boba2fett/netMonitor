#!/usr/bin/env python3
import time
import datetime
import sys, os

def mainloop():
    print(f"Starting netMonitor in {CONFIG['env']}")
    dbApi=DbApi()
    send=Send()
    send.sendInitial(f"Starting netMonitor in {CONFIG['env']}")
    netApi=NetApi()
    send.sendError(dbApi.test())
    lastTimestamp=None
    while True:
        try:
            currtime=time.time()
            distance=300 - currtime % 300
            alligned_time=currtime+distance
            time.sleep(distance) # wait to the next 5 min
            timestamp=datetime.datetime.fromtimestamp(int(alligned_time)) # everyone gets same 5min alligned time
            try:
                data=netApi.getData()
                dbApi.dbCollect(data,timestamp)
                try:
                    send.sendCheck(dbApi,lastTimestamp,timestamp)
                except Exception as e:
                    send.sendError(f"Possible sending messages unsuccesful, because of {str(e)}")
                lastTimestamp=timestamp
            except Exception as e:
                send.sendError(f"DataCollection unsuccesful, because of {str(e)}")
        except Exception as e:
            send.sendError(f"Fail in Mainloop pending 290s, because of {e}")
            time.sleep(290)


if __name__ == '__main__':
    if len(sys.argv)>1 and sys.argv[1]=="dev":
        os.environ['tg-env'] = "dev"
    from config import CONFIG
    from dbapi import DbApi
    from send import Send
    from netapi import NetApi
    import handler
    mainloop()
