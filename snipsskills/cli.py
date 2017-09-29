# -*-: coding utf-8 -*-
""" snipsskills

Usage:
  snipsskills install [--skip_bluetooth --skip_systemd --force_download]
  snipsskills install bluetooth [--force_download]
  snipsskills install skill <skill_url>
  snipsskills install skills [--snipsfile=<snipsfile_path>]
  snipsskills fetch assistant [--snipsfile=<snipsfile_path>] [--id=<id> --url=<url> --file=<file>] [--force_download]
  snipsskills load assistant [--file=<file> --platform_only]
  snipsskills setup microphone [--snipsfile=<snipsfile_path>] [<microphone_id> [--skip_asoundrc] [--update_asoundconf] [PARAMS ...]]
  snipsskills setup systemd bluetooth [--mqtt_host=<mqtt_host> --mqtt_port=<mqtt_port>]
  snipsskills setup systemd snips
  snipsskills setup systemd skills [--snipsfile=<snipsfile_path>]
  snipsskills login
  snipsskills logout
  snipsskills -h | --help
  snipsskills --version

Options:
  -h --help                         Show this screen.
  --version                         Show version.
  --snipsfile=<path>                Path to the Snipsfile.
  --skill=<skillname>

Examples:
  snipsskills install

Help:
  For help using this tool, please open an issue on the Github repository:
  https://github.com/snipsco/snipsskills
"""
# snipsskills setup microphone (--snipsfile | <microphone_id>) [--skip_asoundrc] [--update_asoundconf] [PARAMS ...]
  
#   snipsskills update snips
#   snipsskills install assistant
#   snipsskills scaffold skill_name
#   snipsskills logs
#   snipsskills install
#   snipsskills install skills
#   snipsskills run


#   snipsskills install
#   snipsskills install [--snipsfile=<path> --email=<email> --password=<password> --yes]
#   snipsskills install bluetooth [--bt-mqtt-hostname=<localhost> --bt-mqtt-port=<9898>]
#   snipsskills run
#   snipsskills run [--snipsfile=<path>]
#   snipsskills scaffold


import os
import sys

from docopt import docopt
from snipsskillscore import pretty_printer as pp

from . import __version__ as VERSION

def matches_options(options, option_string):
    values = option_string.split("/")
    for value in values:
        if options[value] != True:
            return False
    return True

def main():
    """ Main entry point. """
    options = docopt(__doc__, version=VERSION)

    try:
      if options['setup'] == True and options['microphone'] == True:
          from snipsskills.commands.setup.microphone import MicrophoneInstaller
          MicrophoneInstaller(options).run()
      elif options['setup'] == True and options['systemd'] == True and options['bluetooth'] == True:
          from snipsskills.commands.setup.systemd.bluetooth import SystemdBluetooth
          SystemdBluetooth(options).run()
      elif options['setup'] == True and options['systemd'] == True and options['snips'] == True:
          from snipsskills.commands.setup.systemd.snips import SystemdSnips
          SystemdSnips(options).run()
      elif options['setup'] == True and options['systemd'] == True and options['skills'] == True:
          from snipsskills.commands.setup.systemd.snipsskills import SystemdSnipsSkills
          SystemdSnipsSkills(options).run()
      elif options['login'] == True:
          from snipsskills.commands.session.login import Login
          Login(options).run()
      elif options['logout'] == True:
          from snipsskills.commands.session.logout import Logout
          Logout(options).run()
      elif options['fetch'] == True and options['assistant'] == True:
          from snipsskills.commands.assistant.fetch import AssistantFetcher
          AssistantFetcher(options).run()
      elif options['load'] == True and options['assistant'] == True:
          from snipsskills.commands.assistant.load import AssistantLoader
          AssistantLoader(options).run()
      elif options['install'] == True and options['bluetooth'] == True:
          from snipsskills.commands.install.bluetooth import BluetoothInstaller
          BluetoothInstaller(options).run()
      elif options['install'] == True and options['skill'] == True:
          from snipsskills.commands.install.skill import SkillInstaller
          SkillInstaller(options).run()
      elif options['install'] == True and options['skills'] == True:
          from snipsskills.commands.install.skills import SkillsInstaller
          SkillsInstaller(options).run()
      elif options['install'] == True:
          from snipsskills.commands.install.install import GlobalInstaller
          GlobalInstaller(options).run()
    except KeyboardInterrupt:
        try:
            print("\n")
            pp.perror("Snips Skills installer interrupted")
            sys.exit(0)
        except SystemExit:
            os._exit(0)

    # elif options['install'] == True:
    #     from snipsskills.commands.install import Install
    #     Install(options).run()
    #     return
    # elif options['run'] == True:
    #     from snipsskills.commands.run import Run
    #     Run(options).run()
    #     return
    # elif options['scaffold'] == True:
    #     from snipsskills.commands.scaffold import Scaffold
    #     Scaffold().run()

if __name__ == '__main__':
    main()