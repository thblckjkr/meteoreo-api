from onesignal_sdk.client import Client
import config.notification as notification

# TODO: Add support for more notification drivers
class NotificationProvider:
  def __init__(self):

    self.client = Client(
        app_id=notification.NOTIFICATIONS['onesignal']['app_id'],
        rest_api_key=notification.NOTIFICATIONS['onesignal']['rest_api_key'],
        user_auth_key=notification.NOTIFICATIONS['onesignal']['user_auth_key'],
    )

  """Builds a notification
  """
  def build(self, error, station, segment = None):
    # station.name
    self.notification = {
        'contents': {
            'en': "Error[%s] en estación %s" % (error, station.name),
            'es': "Error[%s] en estación %s" % (error, station.name),
        },
        'included_segments': ['Active Users', error],
        # 'filters': [
        #     {
        #         'field': 'tag',
        #         'key': 'station_id',
        #         'relation': '=',
        #       'value': station.id
        #     }
        # ]
    }
    return self

  """Sends a notification

  If the notification is a new event, then it will be sent to all users.
  If the notification is an update, and the configuration says to always notificate,
  it will send notification to all users.

  Args:
    is_new_event (bool): True if the notification is a new event
  """

  def send(self, is_new_event = False):
    if is_new_event or (not is_new_event and notification.NOTIFICATIONS['always']):
      try:
        response = self.client.send_notification(self.notification)
        logger.info("Notification sent: %s", response)
      except Error as e:
        logger.error("Error sending notification: %s", str(e))
        raise e
