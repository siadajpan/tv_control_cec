import logging
from datetime import datetime

from tv_control_cec.messages.message_manager import MessageManager
from tv_control_cec.mqtt_client.mqtt_client import MQTTClient
from tv_control_cec.tv_controller.tv_controller import TVController

if __name__ == '__main__':
    now = datetime.now()
    dt_string = now.strftime("%Y_%m_%d__%H_%M_%S")

    logging.basicConfig(filename=f'/home/pi/projects/tv_control_cec/logs/{dt_string}.log',
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.DEBUG)

    logging.info('Starting tv controller')
    tv_controller = TVController()
    tv_controller.start()

    logging.info('Starting mqtt client')
    client = MQTTClient()
    client.connect()

    logging.info('Starting message manager')
    message_manager = MessageManager(client.message_queue, client.publish)
    message_manager.start()

    try:
        client.loop_forever()
    except KeyboardInterrupt:
        tv_controller.stop()
        message_manager.stop()
