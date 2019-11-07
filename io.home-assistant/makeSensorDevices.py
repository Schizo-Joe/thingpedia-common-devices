import os
supported_device_classes = {
  "battery": {
  },
  "humidity": {
  },
  "illuminance": {
  },
  "power": {
  },
  "pressure": {
  },
  "signal_strength": {
  },
  "temperature": {
  },
  "timestamp": {
  },
}

for device, states in supported_device_classes.items():

  args = {
    "device": device,
    "device_name": ''.join([t.capitalize() for t in device.split('-')]),
  }

  if not os.path.isdir(os.path.join(os.getcwd(), "../io.home-assistant.{device}-sensor".format(**args))):
    os.mkdir("../io.home-assistant.{device}-sensor".format(**args))

  manifest_string = """abstract class @io.home-assistant.{device}-sensor
#_[thingpedia_name="{device_name} Sensor"]
#_[thingpedia_description="Interface for Home Assistant's {device_name} Sensor."]
#[license="CC-0"]
#[license_gplcompatible=true]
#[subcategory="home"]
{{
  monitorable query state(out state : Number)
  #_[canonical="{device} sensor state"]
  #_[confirmation="the state of your {device} sensor"]
  #_[formatted=["Your {device} sensor is ${{state}}"]];
}}""".format(**args)
  
  with open("../io.home-assistant.{device}-sensor/manifest.tt".format(**args), "w") as file:
    file.write(manifest_string)

  dataset_string = """dataset @io.home-assistant.{device}-sensor {{
  program := now => @io.home-assistant.{device}-sensor.state() => notify
  #_[utterances="what is the state of my {device} sensor?",
                "what is my {device} sensor showing?",
                "what does my {device} sensor say?",""".format(**args)

  dataset_string = dataset_string[:-1] + """]];"""

  dataset_string += """

  program (p_name : String) := now => @io.home-assistant.{device}-sensor(name=p_name).state() => notify
  #_[utterances="what is the state of my ${{p_name}} {device} sensor?",
                "what is my ${{p_name}} {device} sensor showing?",
                "what does my ${{p_name}} {device} sensor say?",""".format(**args)

  dataset_string = dataset_string[:-1] + """]];"""

  dataset_string += """

  query := @io.home-assistant.{device}-sensor.state()
  #_[utterances="the state of my {device} sensor",""".format(**args)

  dataset_string = dataset_string[:-1] + """]];"""

  dataset_string += """

  query (p_name : String) := @io.home-assistant.{device}-sensor(name=p_name).state()
  #_[utterances="the state of my ${{p_name}} {device} sensor",""".format(**args)


  dataset_string = dataset_string[:-1] + """]];"""

  dataset_string += """

  stream :=  edge( @io.home-assistant.{device}-sensor.state()) on (state == Number)""".format(**args)

  dataset_string = dataset_string[:-1] + """]];""".format(**args)


  with open("../io.home-assistant.{device}-sensor/dataset.tt".format(**args), "w") as file:
    file.write(dataset_string)