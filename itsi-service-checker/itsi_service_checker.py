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
logger = getLogger(logger_name='itsi_service_checker')

# A number is to present the status of an episode
# 2 is in-progress, 5 is closed.
STATUS_INPROGRESS, STATUS_CLOSED = ('2', '5')

class ServiceChecker(CustomGroupActionBase):
    # The name of service URL parameter configured in in alert_actions.conf
    SERVICE_URL_CONFIG_KEY = 'service_url'

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

    def execute(self):
        try:
            service_url = self.get_config().get(self.SERVICE_URL_CONFIG_KEY, '')

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
        except Exception as e:
            logger.error('Failed to check service: %s' % e.message)
            logger.exception(e)
            sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == '--execute':
        input_params = sys.stdin.read()
        serviceChecker = ServiceChecker(input_params)
        serviceChecker.execute()
