# Create a custom alert to send a message to Slack

This custom alert action sends messages to Slack. The files referred to in this README exist in the `splunk-itsi-custom-alerts` repository.

## Create a Splunk app to hold the alert
1. Log in to IT Service Intelligence (ITSI).
1. In the **App** dropdown, click **Manage Apps**.
1. Click **Create app**.
1. Configure the following fields:

Field | Value
------------ | -------------
Name |  ITSI Slack Alert
Folder name | itsi-slack-alert
Version | 1.0.0
Visible | Yes
Author | *Your name*
Template | barebones
Upload asset | *Optional. The asset list provides external information about the devices on your system, such as the asset priority, owner, and business unit.*
  
5. Click **Save**.

A new directory called **itsi-slack-alert**  is created under the `$SPLUNK_HOME/etc/apps` directory. The following list shows the contents of the directory:
```
$ find itsi-slack-alert/
itsi-slack-alert/
itsi-slack-alert/default
itsi-slack-alert/default/data
itsi-slack-alert/default/data/ui
itsi-slack-alert/default/data/ui/views
itsi-slack-alert/default/data/ui/views/README
itsi-slack-alert/default/data/ui/nav
itsi-slack-alert/default/data/ui/nav/default.xml
itsi-slack-alert/default/app.conf
itsi-slack-alert/metadata
itsi-slack-alert/metadata/default.meta
itsi-slack-alert/metadata/local.meta
itsi-slack-alert/bin
itsi-slack-alert/bin/README
itsi-slack-alert/local
itsi-slack-alert/local/app.conf
```
6. On the **Apps** page, search for **itsi-service-checker**.
7. Click **Permissions**.
8. Set **Apply selected role permissions** to **All apps (system)**.

## Update the files to Use the Custom Alert
1. Copy **itsi_sample_slack_alert.py** to `$SPLUNK_HOME/etc/apps/itsi-slack-alert/bin/`.
1. Copy **itsi_sample_slack_alert.html** to `$SPLUNK_HOME/etc/apps/itsi-slack-alert/default/data/ui/alerts/`.
1. Copy **alert_actions.conf** to `$SPLUNK_HOME/etc/apps/itsi-slack-alert/default/`.
1. Copy **alert_actions.conf.spec** to `$SPLUNK_HOME/etc/apps/itsi-slack-alert/README/` (Create the README folder if it doesn't already exist).
1. In order for ITSI to recognize the alert action, open or create a local copy of `notable_event_actions.conf` at `$SPLUNK_HOME/etc/apps/SA-ITOA/local/` and add the the following stanza:
```
[itsi_sample_slack_alert]
disabled = 0
```
6. Restart Splunk software. Navigate to Episode Review in ITSI and confirm that the action named **Slack Alert Action** is listed in the Actions dropdown.
