#! /usr/bin/env python3

__author__ = "Christophe Rime"
__email__ = "christopherime@me.com"
__repository__ = "https://github.com/christopherime/check_AlertManager"
__version__ = "1.1.0"
__description__ = "Nagios plugin to check alerts on AlertManager"

# Nagios dev info https://nagios-plugins.org/doc/guidelines.html
#     Value	    Status
#       0         OK
#       1       Warning
#       2	    Critical
#       3	    Unknown

# Importing modules
from unittest import case
import requests, sys

# Glocabl variables init
critCounter = 0

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
            sys.exit(3)
    except requests.exceptions.RequestException as e:
        print("Error: " + str(e))
        sys.exit(3)

nArgument = len(sys.argv)

# Check if there is any argument, if not print help and quit
if (nArgument - 1) == 0:
    print('No arguments given')
    sys.exit(3)
else:
    # Default values
    hostname = 'localhost'
    critLevelCheck = 2
    altHostname = 0
    tlsEnable = 0
    
    # Check if the first argument is -h or --help then print help and quit
    if sys.argv[1] == '-h' or sys.argv[1] == '--help':
        printHelp()
        
    # Found another target host, will replace hostname with this value
    else:
        hostname = sys.argv[1]
        if nArgument > 2:
            critLevelCheck = sys.argv[2]
            if nArgument > 3:
                altHostname = sys.argv[3]
                if nArgument > 4:
                    tlsEnable = sys.argv[4]

urlToSend = "http://" + str(hostname) + ":9093/api/v2/alerts"  
# Test if there already is and http or https scheme in the URL
if ("http://" in hostname) or ("https://" in hostname):
    urlToSend = str(hostname) + ":9093/api/v2/alerts"  
# If not, add the http scheme from the tls_enable argument
else:
    if tlsEnable == 1:
        urlToSend = "https://" + str(hostname) + ":9093/api/v2/alerts"

alertsList = getAlerts(urlToSend)
infoHostname = altHostname if altHostname != 0 else hostname

#  critLevelCheck == 1 : Critical if ANY alert is raised regardless of the alert severity 
if critLevelCheck == 1:
    print("CRITICAL: " + str(len(alertsList)) + " alerts raised on " + str(infoHostname))
    sys.exit(2)

# critLevelCheck == 2 : Critical if ONLY CRITICAL alerts are raised
elif critLevelCheck == 2:
    
    # Increment critCount for each alert with severity CRITICAL and not suppressed
    for alert in alertsList:
        if (alert['labels']['severity'] == 'critical') and (alert['status']['state'] != 'suppressed'):
            critCounter+=1

    # Checking if there is at least one alert
    if critCounter > 0:
        print("CRITICAL: " + str(critCounter) + " Alerts Detected on " + str(infoHostname))
        sys.exit(2)

# critLevelCheck == 3 : Warning always, this check will always return a warning
elif critLevelCheck == 3:
    # Increment critCount for each alert with severity CRITICAL and not suppressed
    for alert in alertsList:
        if (alert['labels']['severity'] == 'critical') and (alert['status']['state'] != 'suppressed'):
            critCounter+=1

    # Checking if there is at least one alert
    if critCounter > 0:
        print("Warning: " + str(critCounter) + " Alerts Detected on " + str(infoHostname))
        sys.exit(1)    

# critLevelCheck == 4 : Warning if ANY alert is raised regardless if the alert is supressed or not
elif critLevelCheck == 4:
    if len(alertsList) > 0:
        print("WARNING: " + str(len(alertsList)) + " Alerts Detected on " + str(infoHostname))
        sys.exit(1)

# critLevelCheck == 5 : High level of sensibility, just report the number of alerts deteted regardless of the alert severity or if the are suppressed
elif critLevelCheck == 5:
    if len(alertsList) > 0:
        print("CRITICAL: " + str(len(alertsList)) + " alerts raised on " + str(infoHostname))
        sys.exit(2)

else:
    print("Don\'t know what to do with this crit_level")
    sys.exit(3)

# No alert found
print("OK: No alerts detected on " + str(infoHostname))
sys.exit(0)
