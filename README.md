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

``` text
check_AMAlerts.py <alertManager_URL> <crit_level> <alt_hostname> <tls_enable>

Arguments

    -h, --help:  Show this help message and exit

    alertManager_URL:
        URL of the AlertManager instance

    crit_level:
        The sensibility of the check. Default is 2.
            1: Critical if ANY alert is raised regardless of the alert severity
            2: Critical if ONLY CRITICAL alerts are raised
            3: Warning always, this check will return a warning
            4: Warning if ANY alert is raised regardless if the alert is suppressed or not
            5: Critical if ANY alert is raised regardless if the alert is suppressed or not

    alt_hostname:
        Alternative hostname to use in the output. Default is the hostname of the machine.
        If empty localhost will be used.
        
    tls_enable:
        TLS for the hostname. Default is False.
        0: Disable TLS, HTTP scheme will be used
        1: Enable TLS, HTTPS scheme will be used
```
