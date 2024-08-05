import json

from checks import all_checks
from checks.utils.globals import hosts_description

failures = []
hosts = hosts_description
for hostname in hosts:
    try:
        check_name = 'check_%s' % hosts_description[hostname]['backend'].lower()
        print 'Checking host: "%s"' % hostname
        getattr(all_checks, check_name)(hostname)

    except Exception as err:
        failures.append({hostname: str(err.message)})
print '********* Results *********'
if len(failures)>0:
    print json.dumps(failures, indent=2)
