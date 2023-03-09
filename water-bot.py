# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

#My Imports
import os
from confluent_kafka import Producer, Consumer
import pymongo
from dotenv import load_dotenv

load_dotenv(".env")

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

#Connect to Mongo Atlas and set the database to plant-profile and collection to profile
client = pymongo.MongoClient(os.getenv("MONGO_STRING"))
mongoDb = client["plant-profile"]
collection = mongoDb["profile"]
# Find a specific profile in the collection and sets it to the profile variable
profile = collection.find_one({"_id": 1})
myquery = { "_id": 1 }


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Welcome to the water bot"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )
#Gets the latest watering date of the plant and speaks it back to the user    
class WaterDateIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("waterDateIntent")(handler_input)

    def handle(self, handler_input):
        waterDate = collection.find_one({"_id": 1})["date-last-watered"]
        plantName = collection.find_one({"_id": 1})["name"]
        speak_output = "%s was last watered on %s"%(plantName, waterDate)
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )
#Gets the current temperature from the mongo database
class GetTemperatureIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("getTemperatureIntent")(handler_input)

    def handle(self, handler_input):
        sliced = slice(13,-1)
        temp = collection.find_one({"_id": 1})["temperature"]
        temperature = temp[sliced]
        speak_output = "The current room temperature is %s degrees celcius"%(temperature)
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )
#gets the humidity from the mongo database
class GetHumidityIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("getHumidityIntent")(handler_input)

    def handle(self, handler_input):
        sliced = slice(9,-1)
        humid = collection.find_one({"_id": 1})["humidity"]
        humidity = humid[sliced]
        speak_output = "The current room humidity is %s percent"%(humidity)
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )
#Gets the watering type and speak it to the user
class GetWateringTypeIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("getWateringTypeIntent")(handler_input)

    def handle(self, handler_input):
        wateringType = collection.find_one({"_id": 1})["watering-type"]
        speak_output = "The watering type is set to %s based watering"%(wateringType)
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

#Sets the watering type to weekly
class WeeklyWateringIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("weeklyWateringIntent")(handler_input)

    def handle(self, handler_input):
        newvalues = { "$set": { "watering-type": "weekly" } }
        collection.update_one(myquery, newvalues)
        speak_output = "The watering type has been set to weekly"
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )
#sets the watering type to manual
class ManualWateringIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("manualWateringIntent")(handler_input)

    def handle(self, handler_input):
        newvalues = { "$set": { "watering-type": "manual" } }
        collection.update_one(myquery, newvalues)
        speak_output = "The watering type has been set to manual"
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )
#Sets the watering type to moisture based
class MoistureWateringIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("moistureWateringIntent")(handler_input)

    def handle(self, handler_input):
        newvalues = { "$set": { "watering-type": "moisture" } }
        collection.update_one(myquery, newvalues)
        speak_output = "The watering type has been set to moisture-based"
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )
#Sets the watering type to bi-weekly
class BiWeeklyWateringIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("biWeeklyWateringIntent")(handler_input)

    def handle(self, handler_input):
        newvalues = { "$set": { "watering-type": "bi-weekly" } }
        collection.update_one(myquery, newvalues)
        speak_output = "The watering type has been set to bi-weekly"
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# A fun metal gear easter egg
class EasterEggIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("easterEggIntent")(handler_input)

    def handle(self, handler_input):
        
        speak_output = "Why are we still here? Just to suffer? Every night, I can feel their leaves... And their flowers... even their stems... The plants I've lost... the saplings I've lost... won't stop hurting... It's like they're all still there. You feel it too, don't you? I'm gonna make them water our plants!"
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class HelloWorldIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("HelloWorldIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Hello World!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can say a number of different watering system based things to me! How can I help?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class FallbackIntentHandler(AbstractRequestHandler):
    """Single handler for Fallback Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        speech = "Hmm, I'm not sure. You can ask when the plant was watered last or Help. What would you like to do?"
        reprompt = "I didn't catch that. What can I help you with?"

        return handler_input.response_builder.speak(speech).ask(reprompt).response

class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(HelloWorldIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(WaterDateIntentHandler())
sb.add_request_handler(WeeklyWateringIntentHandler())
sb.add_request_handler(MoistureWateringIntentHandler())
sb.add_request_handler(BiWeeklyWateringIntentHandler())
sb.add_request_handler(ManualWateringIntentHandler())
sb.add_request_handler(GetTemperatureIntentHandler())
sb.add_request_handler(GetHumidityIntentHandler())
sb.add_request_handler(GetWateringTypeIntentHandler())
sb.add_request_handler(EasterEggIntentHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()