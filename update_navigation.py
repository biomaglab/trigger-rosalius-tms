import time
import threading
from remote_control import RemoteControl
import constants as consts

class UpdateNavigationInfo:

    def __init__(self):
        '''
        Define information for updating navigation information; characteristics of the object
        '''

        self.rc = None
        self.thread = None
        self.target_status = None
        self.marker_label = None

    def connect(self, address, port):
        self.rc = RemoteControl('http://' + address + ':' + port) # Refers to the first pulse, the Conditioning Stimulus (CS)
        self.rc.try_connect()
        self.call_thread()

    def get_buffer_msg(self):
        '''
        Check the message status in the Buffer that comes from the relay_server
        '''

        while True:
            buffer = self.rc.get_buffer()

            if len(buffer) == 0:
                pass

            for i in range(len(buffer)):
                if buffer[i]['topic'] == consts.PUB_MESSAGES[0]:
                    self.target_status = buffer[i]["data"]["state"]
                elif buffer[i]['topic'] == consts.PUB_MESSAGES[1]:
                    self.marker_label = buffer[i]["data"]["name"]

            time.sleep(0.1)

    def call_thread(self):
        '''
        Call the get_buffer_msg function as a thread
        '''

        self.thread = threading.Thread(target=self.get_buffer_msg, daemon=True)
        self.thread.start()

    #TODO: stop thread
    # def stop_thread(self):

# create_navigation_marker = True
# delete_marker = False
# unset_marker = False
#
# def send_trigger_to_navigation(rc):
#     global create_navigation_marker
#     if create_navigation_marker:
#         topic = 'Create marker'
#         data = {}
#         rc.send_message(topic, data)
#
# def send_to_navigation_delete_marker(rc):
#     global delete_marker
#     if delete_marker:
#         topic = 'Delete marker'
#         data = {'Enabled':'True'}
#         rc.send_message(topic, data)
# def send_to_navigation_unset_marker(rc):
#     global unset_marker
#     if unset_marker:
#         topic = 'Unset marker'
#         data = {'Enabled':'False'}
#         rc.send_message(topic, data)