# Create ITSI Custom Alert to Send Something to Slack
The files refered in this README can be found in 
## Create an Splunk App For Holding the Alert
* Login Splunk in *App* drop down, go to *Manage Apps*, in the new page, click *Create App*
* In the new page, set the following values:
  - Name: *ITSI Slack Alert*
  - Folder Name: *itsi-slack-alert*
  - Version: *1.0.0*
  - Visible: *Yes*
  - Author: *You_name_here*
  - Template: *barebones*
  - Upload asset: *optional*
Now you will have *itsi-slack-alert* created in $SPLUNK_HOME/etc/apps directory, here are the contents created:
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
Go to *Manage Apps*, search for *itsi-slack-alert*, click *Permissions* in the row, and set *Apply selected role permissions to:* *All apps (system)*. 
## Update the files to Use the Custom Alert
- Copy *itsi_sample_slack_alert.py* to *$SPLUNK_HOME/etc/apps/itsi-slack-alert/bin/*.
- Copy *itsi_sample_slack_alert.html* to *$SPLUNK_HOME/etc/apps/itsi-slack-alert/default/data/ui/alerts/*.
- Copy *alert_actions.conf* to *$SPLUNK_HOME/etc/apps/itsi-slack-alert/default/*.
- Copy *alert_actions.conf.spec* to *$SPLUNK_HOME/etc/apps/itsi-slack-alert/README/* (Create the README folder if it doesn't exist).
- In order to make ITSI recognize the alert action, update $SPLUNK_HOME/etc/apps/SA-ITOA/local/notable_event_actions.conf (create this file if doesn't exist) by adding the following lines:
```
[itsi_sample_slack_alert]
disabled = 0
```
## Restart Splunk
Then you will see the action listed in Actions drop down of ITSI Episode Review page.
