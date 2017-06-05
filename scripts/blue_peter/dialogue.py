from naoqi_interfaces.events.event_abstractclass import EventAbstractclass
from animated_say import AnimatedSay
import urllib2


class Dialogue(EventAbstractclass):
    applications = {
        "hug": "hug",
        "highfive": "highfive",
        "dance": "arcadia/full_launcher"
    }
    precanned_text = {
        "about": "I am pepper and I am 1 point 20 meters tall. I live at the Heriot Watt University "
                 "in Edinburgh and am part of the mummer EU project."
    }
    dialogue_name = "pepper_chatbot"

    def __init__(self):
        super(self.__class__, self).__init__(inst=self, event="MyEventData", proxy_name="ALSpeechRecognition")
        self.create_proxy("ALDialog")
        self.create_proxy("ALBehaviorManager")
        self.animated_say = AnimatedSay()
        self.ALDialog.setLanguage("English")
        topic_content = ('topic: ~example_topic_content()\n'
                         'language: enu\n'
                         'concept:(hug) [hug squeeze "bring it in"]\n'
                         'concept:(highfive) ["high five" "give me five" "up top"]\n'
                         'concept:(dance) [dance "show me your moves"]\n'
                         'concept:(about) ["tell me about yourself" "tell me" yourself about]\n'
                         'u: ({*} ~hug {*}) $MyEventData=hug \n'
                         'u: ({*} ~highfive {*}) $MyEventData=highfive \n'
                         'u: ({*} ~dance {*}) $MyEventData=dance \n'
                         'u: ({*} ~about {*}) $MyEventData=about \n'
                         'u: (_*) $MyEventData=$1 \n'
                         )
        self.topic_name = self.ALDialog.loadTopicContent(topic_content)
        self.ALDialog.activateTopic(self.topic_name)
        self.ALDialog.subscribe(self.dialogue_name)

    def callback(self, *args, **kwargs):
        self.ALDialog.unsubscribe(self.dialogue_name)
        try:
            self.execute_application(str(args[1]))
        except KeyError:
            try:
                self.animated_say.say(self.precanned_text[str(args[1])])
            except KeyError:
                self.chat(str(args[1]))
        self.ALDialog.subscribe(self.dialogue_name)

    def chat(self, question):
        question = urllib2.quote(question.encode('UTF-8'))
        call_url = 'http://ec2-54-161-44-218.compute-1.amazonaws.com:5000/?q=%s&sid=MUMMERTEST' % question
        answer = urllib2.urlopen(call_url, timeout=10.).read()
        self.animated_say.say(answer)

    def execute_application(self, task):
        self.ALBehaviorManager.runBehavior(self.applications[task])

    def stop(self):
        self.ALDialog.unsubscribe(self.dialogue_name)

        # Deactivating all topics
        self.ALDialog.deactivateTopic(self.topic_name)

        # now that the dialog engine is stopped and there are no more activated topics,
        # we can unload all topics and free the associated memory
        self.ALDialog.unloadTopic(self.topic_name)
