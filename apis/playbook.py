#encoding: utf-8
import json
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase

import ansible.constants as C

class ResultCallback(CallbackBase):

    def v2_runner_on_ok(self, result, **kwargs):
        print(json.dumps({result._host.name: result._result}))


if __name__ == '__main__':
    Options = namedtuple('Options', ['connection', 'module_path', 'forks', 'become', 'become_method', 'become_user', 'check', 'diff'])
    options = Options(connection='smart', module_path=[], forks=6, become=None, become_method=None, become_user=None, check=False, diff=False)

    loader = DataLoader()
    passwords = {}

    callback = ResultCallback()

    inventory = InventoryManager(loader=loader, sources='hosts.py')

    variable_manager = VariableManager(loader=loader, inventory=inventory)

    source = {
        'hosts' : 'mytest',
        'gather_facts' : 'False',
        'tasks' : [
            {
                'name' : 'shell',
                'shell' : 'ls /',
                'register' : 'result',
            },
            {
                'debug' : {
                    'msg' : ' {{ result.stdout }}',
                }
            }
        ]
    }

    play = Play().load(source, variable_manager=variable_manager, loader=loader)

    tqm = None
    tqm = TaskQueueManager(inventory=inventory,
            variable_manager=variable_manager,
            loader=loader,
            options=options,
            passwords=passwords,
            stdout_callback=callback
        )

    result = tqm.run(play)

    if tqm:
        tqm.cleanup()
