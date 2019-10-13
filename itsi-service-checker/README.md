# Create ITSI Custom Alert to Check Web Service
This custom action will check web service, if the web service return 2XX response, close the episode. Otherwise, set the episode's status to in-progress, and send alert via email to the recipient. The files refered in this README can be found in current folder.
## Create an Splunk App For Holding the Alert
* Login Splunk in *App* drop down, go to *Manage Apps*, in the new page, click *Create App*
* In the new page, set the following values:
  - Name: *ITSI Web Service Checker*
  - Folder Name: *itsi-service-checker*
  - Version: *1.0.0*
  - Visible: *No*
  - Author: *You_name_here*
  - Template: *barebones*
  - Upload asset: *optional*

Now you will have *itsi-service-checker* created in $SPLUNK_HOME/etc/apps directory, here are the contents created:
```
$ find itsi-service-checker/
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
Go to *Manage Apps*, search for *itsi-service-checker*, click *Permissions* in the row, and set *Apply selected role permissions to:* *All apps (system)*. 
## Update the files to Use the Custom Alert
- Copy *itsi_service_checker.py* to *$SPLUNK_HOME/etc/apps/itsi-service-checker/bin/*.
- Copy *itsi_service_checker.html* to *$SPLUNK_HOME/etc/apps/itsi-service-checker/default/data/ui/alerts/*.
- Copy *alert_actions.conf* to *$SPLUNK_HOME/etc/apps/itsi-service-checker/default/*.
- Copy *alert_actions.conf.spec* to *$SPLUNK_HOME/etc/apps/itsi-service-checker/README/* (Create the README folder if it doesn't exist).
- In order to make ITSI recognize the alert action, update $SPLUNK_HOME/etc/apps/SA-ITOA/local/notable_event_actions.conf (create this file if doesn't exist) by adding the following lines:
```
[itsi_service_checker]
disabled = 0
```
## Restart Splunk
Then you will see the action listed in Actions drop down of ITSI Episode Review page.
