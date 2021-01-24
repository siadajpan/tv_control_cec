import logging
from datetime import datetime

from tv_control_cec.messages.message_manager import MessageManager
from tv_control_cec.mqtt_client.mqtt_client import MQTTClient

if __name__ == '__main__':
    now = datetime.now()
    dt_string = now.strftime("%Y_%m_%d__%H_%M_%S")

    logging.basicConfig(
        filename=f'/home/karol/Projects/tv_control_cec/logs/{dt_string}.log',
        filemode='a',
        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
        datefmt='%H:%M:%S',
        level=logging.DEBUG)

    logging.info('Starting mqtt client')
    client = MQTTClient()
    client.connect()

    logging.info('Starting message manager')
    message_manager = MessageManager(client.message_queue, client.publish)
    message_manager.start()

    try:
        client.loop_forever()
    except KeyboardInterrupt:
        message_manager.stop()
