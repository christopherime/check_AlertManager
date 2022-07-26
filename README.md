# check_AlertManager

Plugin in Python3 for Nagios to check the status of alerts on a remote AlertManager.

## Installation

```bash
pip3 install -r requirements.txt
```

## Usage

```bash
check_alertmanager TBD better documentation
```

## Help

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