from rasa_core.channels.slack import SlackInput
from rasa_core.agent import Agent
from rasa_core.interpreter import RasaNLUInterpreter
import yaml
from rasa_core.utils import EndpointConfig


nlu_interpreter = RasaNLUInterpreter('./models/nlu/default/chatter')
action_endpoint = EndpointConfig(url="http://localhost:5056/webhook")
agent = Agent.load('./models/dialogue', interpreter = nlu_interpreter, action_endpoint = action_endpoint)

input_channel = SlackInput('<<token>>' #your bot user authentication token
                           )

agent.handle_channels([input_channel], 5005, serve_forever=True)
