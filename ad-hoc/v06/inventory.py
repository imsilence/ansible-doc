#!/bin/env python3
#encoding: utf-8

inventory = {
    '_meta' : {
        'hostvars' : {
            'localhost' : {
                'ansible_connect' : 'local',
            },
            'mytest' : {
                'ansible_host' : 'xxx.xxx.xxx.xxx',
                'ansible_user' : 'silence',
            }
        }
    },
    'all' : {
        'hosts' : [
            'localhost'
        ],
    },
    'webserver' : {
        'hosts' : [
            'mytest'
        ],
        'vars' : {
            'ansible_connect' : 'smart',
            'ansible_port' : 22,
            'ansible_become_user' : 'root',
            'ansible_python_interpreter' : '/bin/env python2.6'
        }
    }
}

if __name__ == '__main__':
    import json, sys
    print(json.dumps(inventory))
    sys.exit(0)