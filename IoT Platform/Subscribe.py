#http://autobahn.readthedocs.io/en/latest/wamp/programming.html

########---------- Subscribe on topic ------------------###############
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner

class MyComponent(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):
        print("session joined")

        def oncounter(count):
            print("event received: {0}", count)

        try:
            yield self.subscribe(oncounter, u'com.myapp.topic1')
            print("subscribed to topic")
        except Exception as e:
            print("could not subscribe to topic: {0}".format(e))

if __name__ == '__main__':
    runner = ApplicationRunner(url=u"ws://localhost:8008/ws", realm=u"realm1")
    runner.run(MyComponent)



############------------- To publish events:  -----------------##############

# curl -H "Content-Type: application/json" -d '{"topic": "com.myapp.topic1", "args": ["Hello, world"]}' http://127.0.0.1:8008/publish

# import requests
# headers = {'Content-Type': 'application/json'}
# data = '{"topic": "com.myapp.topic1", "args": ["Hello, world"]}'
# requests.post('http://127.0.0.1:8008/publish', headers=headers, data=data)
