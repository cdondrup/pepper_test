from naoqi_interfaces.services.service_proxy import ServiceProxy


class Posture(object):
    postures = ["Crouch",
                "LyingBack",
                "LyingBelly",
                "Sit",
                "SitRelax",
                "Stand",
                "StandInit",
                "StandZero"
                ]

    def __init__(self):
        self.motion = ServiceProxy(proxy_name="ALRobotPosture")

    def go_to_pose(self, name):
        if name not in self.postures:
            raise AttributeError("Unknown posture %s" % name)
        self.motion.goToPosture(name, .8)

    def stand(self):
        self.go_to_pose("Stand")
