#!/usr/bin/python
import requests
import argparse
import json

base_url='https://example.com/munkireport'
login='service_username'
password='service_password'

MR_DATA_QUERY='/datatables/data'

# authenticate and get a session cookie
auth_url ='{0}/auth/login'.format(base_url)
query_url='{0}/datatables/data'.format(base_url)
munkiinfo_url='{0}/module/munkiinfo/get_data'.format(base_url)
session = requests.Session()
auth_request = session.post(auth_url, data={'login': login, 'password': password})

if auth_request.status_code != 200:
    print 'Invalid url!'
    raise SystemExit

def generate_query(method, query):
    method=list(method)
    q = {'columns[{0}][name]'.format(i+1): c for i, c in enumerate(method)}
    q['columns[0][name]'] = 'machine.hostname'
    q['search[value]'] = query
    return q

def run_query(data):
    query_data = session.post(query_url, data=data)
    return query_data.json()

def get_repourl(serial):
    q = session.post('{0}/{1}'.format(munkiinfo_url, serial))
    return q.json()['SoftwareRepoURL'].split('/')[2]

def join_data(data, results):
    queried_methods = [v for k, v in data.items() if 'name' in k]
    d = [dict(zip(queried_methods, x)) for x in results]
    if 'machine.os_version' in queried_methods:
        for x in d:
            os = [x['machine.os_version'][i:i+2] for i in range(0, len(x['machine.os_version']), 2)]
            os[2] = os[2][1:2]
            x['machine.os_version'] = "%s.%s.%s" % (os[0], os[1], os[2])
    return d

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Query the MunkiReport API.')
    parser.add_argument(
        '-q', '--query',
        help='A search term to base the query on. Searches all fields.',
        required=True
    )
    parser.add_argument(
        '-m', '--method',
        help='A method to retrieve.',
        required=False
    )
    args = parser.parse_args()
    query = args.query
    if args.method:
        method = set(a for a in args.method.split(','))
    else:
        method = set([
            "machine.serial_number",
            "machine.machine_desc",
            "machine.os_version",
            "munkireport.manifestname",
            "warranty.status",
            "reportdata.timestamp"
        ])

    method.add('machine.serial_number')
    data = generate_query(method, query)
    query_results = run_query(data)['data']
    if query_results:
        final_data = join_data(data, query_results)
        print json.dumps(final_data)
    else:
        final_data = dict({'error':'no results found'})
