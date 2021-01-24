class Mqtt:
    ADDRESS = '192.168.0.164'
    PORT = 1883
    USERNAME = 'karol'
    PASSWORD = 'klapeczki'
    TOPIC = 'tv/master_bedroom/main/'
    ERROR_TOPIC = 'errors/tv/master_bedroom/main/'


class Messages:
    POWER_ON = 'power_on'
    STANDBY = 'standby'


class OSCommands:
    POWER_ON = "echo 'on 0' | cec-client -s -d 1"
    STANDBY = "echo 'standby 0' | cec-client -s -d 1"
