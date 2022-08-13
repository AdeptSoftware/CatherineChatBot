from datetime import datetime

DISCORD_EPOCH = 1420070400000 # The first second of 2015

def snowflake2date(snowflake):
    return datetime.fromtimestamp(((snowflake >> 22)+DISCORD_EPOCH)/1000)

def timestamp2snowflake(timestamp_sec):
    return (int(timestamp_sec*1000)-DISCORD_EPOCH) << 22

# v = datetime.strptime("01.01.2015 03:00:00", "%d.%m.%Y %H:%M:%S")
# x = timestamp2snowflake(v.timestamp())

# w = snowflake2date(200000000).strftime("%d.%m.%Y %H:%M:%S")
