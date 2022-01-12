from datetime import datetime

def debugmsg(msgtype, msg):
    print('[{}][{}] {}'.format(
        datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        msgtype,
        msg
    ))