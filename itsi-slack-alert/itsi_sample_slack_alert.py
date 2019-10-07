# Make code compatible with both Python 2 and Python 3
from future import standard_library
standard_library.install_aliases()

import sys
import requests

# Add path of ITSI Event Management SDK
from splunk.clilib.bundle_paths import make_splunkhome_path
sys.path.append(make_splunkhome_path(['etc', 'apps', 'SA-ITOA', 'lib']))

# EventGroup represents a group of events
from itsi.event_management.sdk.grouping import EventGroup

# CustomEventActionBase is a base class of actions which contains util functions
from itsi.event_management.sdk.custom_group_action_base import CustomGroupActionBase

# ITSI Logger API to get logger for current python module
from ITOA.setup_logging import getLogger
logger = getLogger(logger_name='itsi_sample_slack_alert')

class SlackAlert(CustomGroupActionBase):
    # The name of Slack URL parameter configured in in alert_actions.conf
    SLACK_URL_CONFIG_KEY = 'slack_url'

    def __init__(self, settings):
        super(SlackAlert, self).__init__(settings, logger)

    def send_slack(self, url, message):
        logger.info('Sending message: %s' % message)
        payload = "{'text': '%s'}" % message
        try:
            res = requests.post(url, data = payload)
            if 200 <= res.status_code < 300:
                logger.info('Slack message sent, HTTP status=%d' % res.status_code)
                return True
            else:
                logger.error('Failed to send Slack message, HTTP status=%d' % res.status_code)
        except Exception as e:
            logger.error('Failed to send Slack message: %s' % e.message)
        return False

    def execute(self):
        try:
            slack_url = self.get_config().get(self.SLACK_URL_CONFIG_KEY, '')
            itsi_episode = EventGroup(self.get_session_key(), logger)
            for data in self.get_group():
                if isinstance(data, Exception):
                    # Generator can yield an Exception
                    # We cannot print the call stack here reliably, because
                    # of how this code handles it, we may have generated an exception elsewhere
                    # Better to present this as an error
                    logger.error(data)
                    raise data

                if not data.get('itsi_group_id'):
                    logger.warning('Event does not have an `itsi_group_id`. No-op.')
                    continue
                group_id = data.get('itsi_group_id')
                group_title = data.get('title')
                group_severity = data.get('severity')
                group_status = data.get('status')

                # Send message to Slack
                if self.send_slack(slack_url, 'Episode(%s, ID=%s, Severity=%s) is in state: %s' %
                                (group_title, group_id, group_severity, group_status)):
                    itsi_episode.create_comment(group_id, 'Slack message sent successfully!')
                else:
                    itsi_episode.create_comment(group_id, 'Failed to send message to Slack!')

        except Exception as e:
            logger.error('Failed to execute slack alert: %s' % e.message)
            logger.exception(e)
            sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == '--execute':
        input_params = sys.stdin.read()
        slackAlert = SlackAlert(input_params)
        slackAlert.execute()

