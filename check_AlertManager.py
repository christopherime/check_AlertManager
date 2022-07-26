#! /usr/bin/env python3

__author__ = "Christophe Rime"
__email__ = "christopherime@me.com"
__repository__ = "https://github.com/christopherime/check_AlertManager"
__version__ = "1.0.1"
__description__ = "Nagios plugin to check alerts on AlertManager"

# Nagios dev info https://nagios-plugins.org/doc/guidelines.html
#     Value	    Status
#       0         OK
#       1       Warning
#       2	    Critical
#       3	    Unknown

# Importing modules
import requests, json, sys

# Function to display the help, will exit the program with status code 0
def printHelp():
    print("""
        Usage: check_AMAlerts.py <alertManager_URL> <crit_level> <alt_hostname> <tls_enable> ...
        arguments:
        
            -h, --help:  Show this help message and exit
            
            alertManager_URL:
                URL of the AlertManager instance
            
            crit_level:  
               Sensibility of the check. Default is 2.
                1: Critical if ANY alert is raised regardless of the alert severity 
                2: Critical if ONLY CRITICAL alerts are raised
                3: Warning always, this check will always return a warning
                4: Warning if ANY alert is raised regardless if the alert is supressed or not
                5: Critical if ANY alert is raised regardless if the alert is supressed or not
            
            alt_hostname:
                Alternative hostname to use in the output. Default is the hostname of the machine.
                If empty localhost will be used.
            
            tls_enable:
                TLS for hostname. Default is False.
                0: Disable TLS, http scheme will be used
                1: Enable TLS, https scheme will be used
                
        """)
    sys.exit(0)

# Function that make HTTP GET request to and URL
def getAlerts(url):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return r.json()
        else:
            print("Error: " + str(r.status_code))
            sys.exit(2)
    except requests.exceptions.RequestException as e:
        print("Error: " + str(e))
        sys.exit(2)

# Check if there is any argument, if not print help and quit
if (len(sys.argv)-1) == 0:
    print('No arguments given\n')
    printHelp()
else:
    # Default hostname is 'localhost'
    hostname = 'localhost'
    # Check if the first argument is -h or --help then print help and quit
    if sys.argv[1] == '-h' or sys.argv[1] == '--help':
        printHelp()
        
    # Found another target host, will replace hostname with this value
    else:
        hostname = sys.argv[1]
        
# Test if there already is and http or https scheme in the URL
if ("http://" in hostname) or ("https://" in hostname):
    alertsList = getAlerts(hostname + ":9093/api/v2/alerts")
# If not, add the http scheme from the tls_enable argument
else:
    if sys.argv[4] == 1:
        alertsList = getAlerts("https://" + hostname + ":9093/api/v2/alerts")
    else:
        alertsList = getAlerts("http://" + hostname + ":9093/api/v2/alerts")


countAlerts = len(alertsList)
print(countAlerts)

# For each alert in alertsList print the alert name and the alert status
critCounter = 0
for alert in alertsList:
    if (alert['labels']['severity'] == 'critical') and (alertsList[0]['status']['state'] != 'suppressed'):
        critCounter +1
        
# Checking if there is at least one alert
if critCounter > 0:
    print("Alerts Detected on " + hostname)
    sys.exit(2)

# No alert found
print('No alerts')
sys.exit(0)
