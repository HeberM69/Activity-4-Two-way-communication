class Ontology:
  def _init_(self):
      self.beliefs = {
          'location': ['A', 'B', 'C', 'D', 'E'],
          'current_location': None,
          'route': [],
          'current_index': 0 
      }

class Agent:
  def _init_(self, name):
      self.name = name
      self.position = None
      self.beliefs = Ontology()

  def move(self, destination):
      self.position = destination

  def perceive_environment(self):
      print(f"{self.name} perceives the environment")

  def decide_action(self):
      print(f"{self.name} decides the action")

  def communicate(self, message):
      print(f"{self.name} communicates: {message}")

  def request_action(self, agent, action):
      message = {"performative": "request", "content": {"action": action}}
      agent.receive_message(message)

  def receive_message(self, message):
      pass

class DriverAgent(Agent):
  def _init_(self, name):
      super()._init_(name)

  def generate_route(self):
      locations = self.beliefs.beliefs['location']
      route = self.beliefs.beliefs['route']
      current_location = self.beliefs.beliefs['current_location']

      while len(route) < 5 or len(set(route)) < 3 or route[0] != route[-1]:
          destination = random.choice(locations)
          if destination != current_location:
              route.append(destination)

  def lead_vehicle(self, vehicle):
      print(f"{self.name} is leading the vehicle")
      self.generate_route()
      route = self.beliefs.beliefs['route']
      self.beliefs.beliefs['current_location'] = route[0]
      self.request_action(vehicle, f"Move to {route[0]}")

  def receive_message(self, message):
      if message["performative"] == "inform":
          print(f"{self.name} received inform: {message['content']}")

class VehicleAgent(Agent):
  def _init_(self, name):
      super()._init_(name)

  def execute_action(self, action):
      print(f"{self.name} executes action: {action}")
      self.communicate("Action executed")

  def receive_message(self, message):
      if message["performative"] == "request":
          action = message["content"]["action"]
          self.execute_action(action)
          reply = {"performative": "inform", "content": "Action completed"}
          self.communicate(reply['content'])

import random

driver = DriverAgent('Driver')
vehicle = VehicleAgent('Vehicle')

driver.position = 'A'
vehicle.position = 'A'
driver.beliefs.beliefs['current_location'] = 'A'
vehicle.beliefs.beliefs['current_location'] = 'A'

driver.perceive_environment()
driver.decide_action()
driver.lead_vehicle(vehicle)
