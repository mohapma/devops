#!/usr/bin/python
# -*- coding: utf-8 -*-
# (c) 2017, Pieter Lexis <pieter.lexis () powerdns.com>
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
#

DOCUMENTATION = '''
---
module: json_file
short_description: Tweak settings in JSON files
extends_documentation_fragment: files
description:
     - Manage (add, remove, change) individual settings in an JSON-style file without having
       to manage the file as a whole with, say, M(template) or M(assemble). Adds missing
       sections if they don't exist.
version_added: "2.4"
options:
  dest:
    description:
      - Path to the JSON-style file; this file is created if required
    required: true
    default: null
  key:
    description:
      - The key to alter in the JSON file. This is added if C(state=present)
        automatically. Key hierarchy is supported, seperate levels with '.' (
        dots in key-names can be escaped with '\.')
    required: true
    default: null
  value:
    description:
     - the value to be associated with the I(key). May be omitted when removing a I(key).
    required: false
    default: null
  as_string:
    description:
    - should the I(value) be added as a string?
    default: false
  backup:
    description:
      - Create a backup file including the timestamp information so you can get
        the original file back if you somehow clobbered it incorrectly.
    required: false
    default: "no"
    choices: [ "yes", "no" ]
  others:
     description:
       - all arguments accepted by the M(file) module also work here
     required: false
  state:
     description:
       - If set to C(absent) the key will be removed.
     required: false
     default: "present"
     choices: [ "present", "absent" ]
  create:
     required: false
     choices: [ "yes", "no" ]
     default: "yes"
     description:
       - If set to 'no', the module will fail if the file does not already exist.
         By default it will create the file if it is missing.
author:
    - "Pieter Lexis (@lieter_)"
'''

EXAMPLES = '''
# Ensure "foo: 'bar'" in specified file
- json_file: dest=/etc/conf key=foo value=bar mode=0600 backup=yes

# Remove the 'buzz' key that is in the 'foo' key
- json_file: dest=/etc/anotherconf
            key=foo.buzz
            state=absent
'''

import os
import re

def _to_type(t):
    """ Returns `t` in the proper format, e.g. an int or a bool"""
    if t.isdigit():
        return int(t)
    if t == 'null' or t == 'None':
        return None
    if t == 'false' or t == 'False':
        return False
    if t == 'true' or t == 'True':
        return True
    return t

def _json_dumps(s):
    """ Returns the JSON-serialized version of `s` as a str"""
    return json.dumps(s, indent=2, separators=(',', ': '), sort_keys=False)

def do_json(module, filename, key, value=None, as_string=False, state='present', create=False, backup=False):
    diff = {'before': '',
            'after': ''}

    if not os.path.exists(filename):
        if not create:
            module.fail_json(rc=257, msg='Destination %s does not exist !' % filename)
        destpath = os.path.dirname(filename)
        if not os.path.exists(destpath) and not module.check_mode:
            os.makedirs(destpath)
        obj = json.loads('{}')
    else:
        json_file = open(filename, 'r')
        try:
            obj = json.load(json_file)
        finally:
            json_file.close()

    if module._diff:
        diff['before'] = _json_dumps(obj)

    changed = False
    msg = 'OK'

    # check for escaped dotted key names
    parts = re.split(r'(?<!\\)\.', key)
    parts = [part.replace('\.', '.') for part in parts]

    # Create keys if the do not exist
    ref = obj
    absent_ok = False
    for part in parts[:-1]:
        if part not in ref:
            # Don't create any elements if we should remove this key
            if state == 'absent':
                absent_ok = True
                break
            ref[part] = {}
        ref = ref[part]

    if state == 'absent' and not absent_ok:
        try:
            del(ref[parts[-1]])
            changed = True
        except KeyError:
            # it was already gone
            pass
    elif state == 'present':
        val = value
        if not as_string:
            val = _to_type(value)
        if parts[-1] not in ref:
            ref[parts[-1]] = val
            changed = True
        if ref.get(parts[-1]) != val:
            ref[parts[-1]] = val
            changed = True

    if module._diff:
        diff['after'] = _json_dumps(obj)

    backup_file = None
    if changed and not module.check_mode:
        if backup:
            backup_file = module.backup_local(filename)
        json_file = open(filename, 'w')
        try:
            json.dump(obj, json_file, indent=2, separators=(',', ': '),
                      sort_keys=False)

        finally:
            json_file.close()

    return (changed, backup_file, diff, msg)

# ==============================================================
# main

def main():

    module = AnsibleModule(
        argument_spec=dict(
            dest=dict(required=True),
            key=dict(required=True),
            value=dict(required=False),
            as_string=dict(default='no', type='bool'),
            backup=dict(default='no', type='bool'),
            state=dict(default='present', choices=['present', 'absent']),
            create=dict(default=True, type='bool')
        ),
        add_file_common_args=True,
        supports_check_mode=True
    )

    dest = os.path.expanduser(module.params['dest'])
    key = module.params['key']
    value = module.params['value']
    state = module.params['state']
    backup = module.params['backup']
    create = module.params['create']
    as_string = module.params['as_string']

    (changed, backup_file, diff, msg) = do_json(module, dest, key, value, as_string, state, create, backup)

    if not module.check_mode and os.path.exists(dest):
        file_args = module.load_file_common_arguments(module.params)
        changed = module.set_fs_attributes_if_different(file_args, changed)

    results = {'changed': changed, 'msg': msg, 'dest': dest, 'diff': diff}
    if backup_file is not None:
        results['backup_file'] = backup_file

    # Mission complete
    module.exit_json(**results)

# import module snippets
from ansible.module_utils.basic import *
if __name__ == '__main__':
    main()
