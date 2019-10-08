import sys
import requests
import splunk.rest as splunk_rest

# Add path of ITSI Event Management SDK
from splunk.clilib.bundle_paths import make_splunkhome_path
sys.path.append(make_splunkhome_path(['etc', 'apps', 'SA-ITOA', 'lib']))

# Make code compatible with both Python 2 and Python 3
import itsi_path
from itsi_py23 import _
import itsi_py23

# EventGroup is the object to manage episodes
from itsi.event_management.sdk.grouping import EventGroup

# CustomEventActionBase is a base class of actions which contains util functions
from itsi.event_management.sdk.custom_group_action_base import CustomGroupActionBase

# ITSI Logger API to get logger for current python module
from ITOA.setup_logging import getLogger
logger = getLogger(logger_name='itsi_service_checker')

from splunk.util import safeURLQuote

# A number is to present the status of an episode
# 2 is in-progress, 5 is closed.
STATUS_INPROGRESS, STATUS_CLOSED = ('2', '5')

class ServiceChecker(CustomGroupActionBase):
    # The name of service URL parameter configured in alert_actions.conf
    SERVICE_URL_CONFIG_KEY = 'service_url'

    # The name of email address parameter configured in alert_actions.conf
    EMAIL_CONFIG_KEY = 'email'

    def __init__(self, settings):
        super(ServiceChecker, self).__init__(settings, logger)

    def check_service(self, url):
        try:
            res = requests.get(url)
            if 200 <= res.status_code < 300:
                logger.info('Service checked, HTTP status=%d' % res.status_code)
                return True
            else:
                logger.error('Service checking returns error, HTTP status=%d' % res.status_code)
        except Exception as e:
            logger.error('Failed to check service: %s' % e.message)
        return False

    def send_email(self, group_ids, emailto, subject, message):
        search_cmd = 'search index="itsi_grouped_alerts" itsi_group_id IN %s | sendemail "email" content_type="html" ' \
                     'to="%s" subject="%s" server="localhost" message="%s" sendresults=true' \
                     % (str(tuple(group_ids)).replace('\'', '"'), emailto, subject, message)
        data = {
            'earliestTime': '-24h',
            'latestTime': 'now',
            'search': search_cmd,
            'exec_mode': 'oneshot',
            'output_mode': 'json'
        }
        logger.info('Running search command: %s to send email' % search_cmd)
        response, content = splunk_rest.simpleRequest(safeURLQuote('/servicesNS/nobody/%s/search/jobs/' %
                                                                    self.settings.get('app')),
                                                      sessionKey=self.get_session_key(),
                                                      method='POST',
                                                      postargs=data)
        if 200 <= response.status < 300:
            logger.info('sendemail command run successfully.')
            return True
        else:
            logger.error('Failed to run sendemail')
        return False

    def execute(self):
        try:
            service_url = self.get_config().get(self.SERVICE_URL_CONFIG_KEY, '')
            email_addr = self.get_config().get(self.EMAIL_CONFIG_KEY, '')

            # The object to manage ITSI episodes
            itsi_episode = EventGroup(self.get_session_key(), logger)

            # The groups that pass the check
            groups_passed = []
            # The groups that fail for the check
            groups_failed = []

            for data in self.get_group():
                if isinstance(data, Exception):
                    # Generator can yield an Exception here
                    logger.error(data)
                    raise data

                if not data.get('itsi_group_id'):
                    logger.warning('Event does not have an `itsi_group_id`. No-op.')
                    continue
                group_id = data.get('itsi_group_id')
                group_title = data.get('title')

                # Check web service
                if self.check_service(service_url):
                    groups_passed.append(group_id)
                    itsi_episode.create_comment(group_id, 'Service check successfully for `%s`,closing it.' %
                                                group_title)
                else:
                    groups_failed.append(group_id)
                    itsi_episode.create_comment(group_id, 'Service check failed for `%s`, putting it in-progress.' %
                                                group_title)

                if groups_passed:
                    itsi_episode.update_status(groups_passed, STATUS_CLOSED)

                if groups_failed:
                    itsi_episode.update_status(groups_failed, STATUS_INPROGRESS)
                    self.send_email(groups_failed, email_addr,
                                    "%s Episodes Failed for Service Check" % len(groups_failed),
                                    "See attachment for relevant events")
        except Exception as e:
            logger.error('Failed to check service: %s' % e.message)
            logger.exception(e)
            sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == '--execute':
        input_params = sys.stdin.read()
        serviceChecker = ServiceChecker(input_params)
        serviceChecker.execute()

