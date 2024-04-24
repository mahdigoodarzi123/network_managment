import os

def rdp(ip, username, password):
    command = f'cmdkey /generic:"{ip}" /user:"{username}" /pass:"{password}" & mstsc /v:{ip}'
    os.system(command)
