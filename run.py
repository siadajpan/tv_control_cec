import logging
from datetime import datetime

from mqtt_utils.message_manager import MessageManager

from tv_control_cec.messages.tv_on import TVOn
from tv_control_cec.messages.tv_standby import TVStandby
from tv_control_cec.settings import settings

if __name__ == '__main__':
    now = datetime.now()
    dt_string = now.strftime("%Y_%m_%d__%H_%M_%S")

    logging.basicConfig(
        filename=f'/home/pi/projects/tv_control_cec/logs/{dt_string}.log',
        filemode='a',
        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
        datefmt='%H:%M:%S',
        level=logging.DEBUG)

    MESSAGES = [TVOn(), TVStandby()]
    message_manager = MessageManager(MESSAGES)
    message_manager.update_credentials(settings.Mqtt.USERNAME,
                                       settings.Mqtt.PASSWORD)
    message_manager.connect(settings.Mqtt.ADDRESS, settings.Mqtt.PORT)

    logging.info('Starting message manager')
    message_manager.start()

    try:
        message_manager.loop_forever()
    except KeyboardInterrupt:
        message_manager.stop()
