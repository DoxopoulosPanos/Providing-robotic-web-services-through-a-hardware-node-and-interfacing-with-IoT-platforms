import requests


########---------- Subscribe on topic ------------------###############
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner

class MyComponent(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):
        print("session joined")

        def oncounter(count):
            #print("event received: {0}", count)

            try:
                internal_temperature = float(count)
                print('internal_temperature: {}'.format(internal_temperature))
                result = requests.get("http://localhost:8080/Mashape/WeatherAPI", params={"lat":40.6, "lng":22.9})
                my_string = result.text
                #keep only the temperature
                new_string = [x.strip() for x in my_string.split(',')] #split by commas
                new_string = [x.strip() for x in new_string[0].split(' ')] #split by spaces
                external_temperature = int(new_string[0])
                print('external_temperature: {}'.format(external_temperature))
                #print "external_temperature: " + external_temperature
                if internal_temperature > external_temperature :
                    print("Outside is cooler than inside!")
            except ValueError:
                #print "Not a float"
                pass
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
