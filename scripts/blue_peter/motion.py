from naoqi_interfaces.services.service_proxy import ServiceProxy


class Motion(object):
    def __init__(self):
        self.motion = ServiceProxy(proxy_name="ALMotion")

    def start_breathing(self):
        self.motion.setBreathEnabled("Arms", True)

    def stop_breathing(self):
        self.motion.setBreathEnabled("Arms", False)
