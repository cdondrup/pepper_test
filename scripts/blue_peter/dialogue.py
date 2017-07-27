from naoqi_interfaces.events.event_abstractclass import EventAbstractclass
from animated_say import AnimatedSay
import urllib2
import random


class Dialogue(EventAbstractclass):
    DIALOGUE_NAME = "pepper_chatbot"

    def init(self, *args):
        self.parser = args[0]
        self.create_proxy("ALDialog")
        self.create_proxy("ALBehaviorManager")
        self.animated_say = AnimatedSay()
        self.ALDialog.setLanguage("English")
        topic_content = ('topic: ~my_autonomous_pepper()\n'
                         'language: enu\n'
                         + self.parser.concepts
                         + self.parser.generate_rules(self.__event__) +
                         'u: (_*) $'+self.__event__+'=$1 \n'
                         )
        self.topic_name = self.ALDialog.loadTopicContent(topic_content)
        self.ALDialog.activateTopic(self.topic_name)
        self.ALDialog.subscribe(self.DIALOGUE_NAME)

    def callback(self, *args, **kwargs):
        self.ALDialog.unsubscribe(self.DIALOGUE_NAME)
        try:
            self.execute_application(str(args[1]))
        except KeyError:
            try:
                self.animated_say.say(random.choice(self.parser.precanned_text[str(args[1])]))
            except KeyError:
                self.chat(str(args[1]))
        self.ALDialog.subscribe(self.DIALOGUE_NAME)

    def chat(self, question):
        question = urllib2.quote(question.encode('UTF-8'))
        call_url = 'http://ec2-54-161-44-218.compute-1.amazonaws.com:5000/?q=%s&sid=MUMMERTEST' % question
        print call_url
        try:
            answer = urllib2.urlopen(call_url, timeout=10.).read()
        except:
            return
        self.animated_say.say(answer)

    def execute_application(self, task):
        self.ALBehaviorManager.runBehavior(self.parser.applications[task])

    def stop(self):
        self.ALDialog.unsubscribe(self.DIALOGUE_NAME)

        # Deactivating all topics
        self.ALDialog.deactivateTopic(self.topic_name)

        # now that the dialog engine is stopped and there are no more activated topics,
        # we can unload all topics and free the associated memory
        self.ALDialog.unloadTopic(self.topic_name)
