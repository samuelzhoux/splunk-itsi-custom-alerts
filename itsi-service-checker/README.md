# Create a custom ITSI alert to check your web service 
This custom action checks the status of your web service. If the web service returns a 2xx response, it closes the episode. Otherwise, it sets the episode's status to "In Progress" and sends an alert via email to a specified recipient. The files referred to in this README exist in the `splunk-itsi-custom-alerts` repository.
## Create a Splunk app to hold the alert
1. Log in to IT Service Intelligence (ITSI).
1. In the **App** dropdown, click **Manage Apps**.
1. Click **Create app**.
1. Configure the following fields:

Field | Value
------------ | -------------
Name |  ITSI Web Service Checker
Folder name | itsi-service-checker
Version | 1.0.0
Visible | No
Author | *Your name*
Template | barebones
Upload asset | *Optional. The asset list provides external information about the devices on your system, such as the asset priority, owner, and business unit.*
  
5. Click **Save**.

A new directory called **itsi-service-checker**  is created under the `$SPLUNK_HOME/etc/apps` directory. The following list shows the contents of the directory:

```
itsi-service-checker/
itsi-service-checker/default
itsi-service-checker/default/data
itsi-service-checker/default/data/ui
itsi-service-checker/default/data/ui/views
itsi-service-checker/default/data/ui/views/README
itsi-service-checker/default/data/ui/nav
itsi-service-checker/default/data/ui/nav/default.xml
itsi-service-checker/default/app.conf
itsi-service-checker/metadata
itsi-service-checker/metadata/default.meta
itsi-service-checker/metadata/local.meta
itsi-service-checker/bin
itsi-service-checker/bin/README
itsi-service-checker/local
itsi-service-checker/local/app.conf
```
6. On the **Apps** page, search for **itsi-service-checker**.
7. Click **Permissions**.
8. Set **Apply selected role permissions** to **All apps (system)**.

## Update the files to use the custom alert

1. Copy **itsi_service_checker.py** to `$SPLUNK_HOME/etc/apps/itsi-service-checker/bin/`.
1. Copy **itsi_service_checker.html** to `$SPLUNK_HOME/etc/apps/itsi-service-checker/default/data/ui/alerts/`.
1. Copy **alert_actions.conf** to `$SPLUNK_HOME/etc/apps/itsi-service-checker/default/`.
1. Copy **alert_actions.conf.spec** to `$SPLUNK_HOME/etc/apps/itsi-service-checker/README/` (Create the README folder if it doesn't already exist).
1. In order for ITSI to recognize the alert action, open or create a local copy of `notable_event_actions.conf` at `$SPLUNK_HOME/etc/apps/SA-ITOA/local/` and add the the following stanza:
```
[itsi_service_checker]
disabled = 0
```
6. Restart Splunk software. Navigate to Episode Review in ITSI and confirm that the action named **Web Service Checker** is listed in the Actions dropdown.
