# Slash command for Slack to display MunkiReport info.

## Setup
### mr_api.py
Set the following for your environment:
```
base_url='https://example.com/munkireport'
login='service_username'
password='service_password'
```
### slack.php
```
$client_url = 'https://example.com/munkireport/clients/detail';
```
The `$post` line can be changed for testing/debugging.

### Your Slack instance
Go to https://your-team.slack.com/apps/manage and select `Slash Commands` and `Add Configuration`.

Choose a name for your command, e.g., `/mr` and fill out all the information, including where you're hosting `slack.php`.

## Usage
There are two ways of calling the command. By itself, a hostname will return the following:
```
"machine.serial_number",
"machine.machine_desc",
"machine.os_version",
"munkireport.manifestname",
"warranty.status",
"reportdata.timestamp"
```
Or you can specify column names separated by commas.
```
/mr column.name1,column.name2 hostname
```
## Screenshots
![Screenshot](/screenshots/screenshot1.png?raw=true "Screenshot")
