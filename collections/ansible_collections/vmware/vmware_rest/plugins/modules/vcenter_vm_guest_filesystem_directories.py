#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2021, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# template: header.j2
# This module is autogenerated by vmware_rest_code_generator.
# See: https://github.com/ansible-collections/vmware_rest_code_generator
from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = r"""
module: vcenter_vm_guest_filesystem_directories
short_description: Creates a directory in the guest operating system
description: Creates a directory in the guest operating system. <p>
options:
    create_parents:
        description:
        - Whether any parent directories should be created.  If any failure occurs,
            some parent directories could be left behind.
        type: bool
    credentials:
        description:
        - The guest authentication data. This parameter is mandatory.
        - 'Valid attributes are:'
        - ' - C(interactive_session) (bool): If {@term set}, theoperation will interact
            with the logged-in desktop session in the guest. This requires that the
            logged-on user matches the user specified by the {@link Credentials}.
            This is currently only supported for {@link Type#USERNAME_PASSWORD}. ([''absent'',
            ''create_temporary'', ''move'', ''present''])'
        - '   This key is required with [''absent'', ''create_temporary'', ''move'',
            ''present''].'
        - ' - C(type) (str): Types of guest credentials ([''absent'', ''create_temporary'',
            ''move'', ''present''])'
        - '   This key is required with [''absent'', ''create_temporary'', ''move'',
            ''present''].'
        - '   - Accepted values:'
        - '     - SAML_BEARER_TOKEN'
        - '     - USERNAME_PASSWORD'
        - ' - C(user_name) (str): For {@link Type#SAML_BEARER_TOKEN}, this is the
            guest user to be associated with the credentials. For {@link Type#USERNAME_PASSWORD}
            this is the guest username. ([''absent'', ''create_temporary'', ''move'',
            ''present''])'
        - ' - C(password) (str): password ([''absent'', ''create_temporary'', ''move'',
            ''present''])'
        - ' - C(saml_token) (str): SAML Bearer Token ([''absent'', ''create_temporary'',
            ''move'', ''present''])'
        required: true
        type: dict
    new_path:
        description:
        - The complete path to where the directory is moved or its new name. It cannot
            be a path to an existing directory or an existing file. Required with
            I(state=['move'])
        type: str
    parent_path:
        description:
        - The complete path to the directory in which to create the new directory.
        type: str
    path:
        description:
        - The complete path to the directory to be created. Required with I(state=['absent',
            'move', 'present'])
        type: str
    prefix:
        description:
        - The prefix to be given to the new temporary directory. Required with I(state=['create_temporary'])
        type: str
    recursive:
        description:
        - If true, all files and subdirectories are also deleted. If false, the directory
            must be empty for the operation to succeed.
        type: bool
    session_timeout:
        description:
        - 'Timeout settings for client session. '
        - 'The maximal number of seconds for the whole operation including connection
            establishment, request sending and response. '
        - The default value is 300s.
        type: float
        version_added: 2.1.0
    state:
        choices:
        - absent
        - create_temporary
        - move
        - present
        default: present
        description: []
        type: str
    suffix:
        description:
        - The suffix to be given to the new temporary directory. Required with I(state=['create_temporary'])
        type: str
    vcenter_hostname:
        description:
        - The hostname or IP address of the vSphere vCenter
        - If the value is not specified in the task, the value of environment variable
            C(VMWARE_HOST) will be used instead.
        required: true
        type: str
    vcenter_password:
        description:
        - The vSphere vCenter password
        - If the value is not specified in the task, the value of environment variable
            C(VMWARE_PASSWORD) will be used instead.
        required: true
        type: str
    vcenter_rest_log_file:
        description:
        - 'You can use this optional parameter to set the location of a log file. '
        - 'This file will be used to record the HTTP REST interaction. '
        - 'The file will be stored on the host that run the module. '
        - 'If the value is not specified in the task, the value of '
        - environment variable C(VMWARE_REST_LOG_FILE) will be used instead.
        type: str
    vcenter_username:
        description:
        - The vSphere vCenter username
        - If the value is not specified in the task, the value of environment variable
            C(VMWARE_USER) will be used instead.
        required: true
        type: str
    vcenter_validate_certs:
        default: true
        description:
        - Allows connection when SSL certificates are not valid. Set to C(false) when
            certificates are not trusted.
        - If the value is not specified in the task, the value of environment variable
            C(VMWARE_VALIDATE_CERTS) will be used instead.
        type: bool
    vm:
        description:
        - Virtual Machine to perform the operation on. This parameter is mandatory.
        required: true
        type: str
author:
- Ansible Cloud Team (@ansible-collections)
version_added: 2.0.0
requirements:
- vSphere 7.0.2 or greater
- python >= 3.6
- aiohttp
notes:
- Tested on vSphere 7.0.2
"""

EXAMPLES = r"""
- name: Create a VM
  vmware.vmware_rest.vcenter_vm:
    placement:
      cluster: "{{ lookup('vmware.vmware_rest.cluster_moid', '/my_dc/host/my_cluster') }}"
      datastore: "{{ lookup('vmware.vmware_rest.datastore_moid', '/my_dc/datastore/local') }}"
      folder: "{{ lookup('vmware.vmware_rest.folder_moid', '/my_dc/vm') }}"
      resource_pool: "{{ lookup('vmware.vmware_rest.resource_pool_moid', '/my_dc/host/my_cluster/Resources') }}"
    name: test_vm1
    guest_OS: RHEL_7_64
    hardware_version: VMX_11
    memory:
      hot_add_enabled: true
      size_MiB: 1024
    disks:
    - type: SATA
      backing:
        type: VMDK_FILE
        vmdk_file: '[local] test_vm1/{{ disk_name }}.vmdk'
    - type: SATA
      new_vmdk:
        name: second_disk
        capacity: 32000000000
    cdroms:
    - type: SATA
      sata:
        bus: 0
        unit: 2
    nics:
    - backing:
        type: STANDARD_PORTGROUP
        network: "{{ lookup('vmware.vmware_rest.network_moid', '/my_dc/network/VM Network') }}"
  register: my_vm

- name: Create a directory in /tmp
  vmware.vmware_rest.vcenter_vm_guest_filesystem_directories:
    vm: '{{ my_vm.id }}'
    path: /tmp/my/path
    create_parents: true
    credentials:
      interactive_session: false
      type: USERNAME_PASSWORD
      user_name: root
      password: root
"""

RETURN = r"""
"""

# This structure describes the format of the data expected by the end-points
PAYLOAD_FORMAT = {
    "move": {
        "query": {},
        "body": {"credentials": "credentials", "new_path": "new_path", "path": "path"},
        "path": {"vm": "vm"},
    },
    "create": {
        "query": {},
        "body": {
            "create_parents": "create_parents",
            "credentials": "credentials",
            "path": "path",
        },
        "path": {"vm": "vm"},
    },
    "delete": {
        "query": {},
        "body": {
            "credentials": "credentials",
            "path": "path",
            "recursive": "recursive",
        },
        "path": {"vm": "vm"},
    },
    "create_temporary": {
        "query": {},
        "body": {
            "credentials": "credentials",
            "parent_path": "parent_path",
            "prefix": "prefix",
            "suffix": "suffix",
        },
        "path": {"vm": "vm"},
    },
}  # pylint: disable=line-too-long

import json
import socket
from ansible.module_utils.basic import env_fallback

try:
    from ansible_collections.cloud.common.plugins.module_utils.turbo.exceptions import (
        EmbeddedModuleFailure,
    )
    from ansible_collections.cloud.common.plugins.module_utils.turbo.module import (
        AnsibleTurboModule as AnsibleModule,
    )

    AnsibleModule.collection_name = "vmware.vmware_rest"
except ImportError:
    from ansible.module_utils.basic import AnsibleModule
from ansible_collections.vmware.vmware_rest.plugins.module_utils.vmware_rest import (
    build_full_device_list,
    exists,
    gen_args,
    get_device_info,
    get_subdevice_type,
    list_devices,
    open_session,
    prepare_payload,
    update_changed_flag,
    session_timeout,
)


def prepare_argument_spec():
    argument_spec = {
        "vcenter_hostname": dict(
            type="str", required=True, fallback=(env_fallback, ["VMWARE_HOST"]),
        ),
        "vcenter_username": dict(
            type="str", required=True, fallback=(env_fallback, ["VMWARE_USER"]),
        ),
        "vcenter_password": dict(
            type="str",
            required=True,
            no_log=True,
            fallback=(env_fallback, ["VMWARE_PASSWORD"]),
        ),
        "vcenter_validate_certs": dict(
            type="bool",
            required=False,
            default=True,
            fallback=(env_fallback, ["VMWARE_VALIDATE_CERTS"]),
        ),
        "vcenter_rest_log_file": dict(
            type="str",
            required=False,
            fallback=(env_fallback, ["VMWARE_REST_LOG_FILE"]),
        ),
        "session_timeout": dict(
            type="float",
            required=False,
            fallback=(env_fallback, ["VMWARE_SESSION_TIMEOUT"]),
        ),
    }

    argument_spec["create_parents"] = {"type": "bool"}
    argument_spec["credentials"] = {"required": True, "type": "dict"}
    argument_spec["new_path"] = {"type": "str"}
    argument_spec["parent_path"] = {"type": "str"}
    argument_spec["path"] = {"type": "str"}
    argument_spec["prefix"] = {"type": "str"}
    argument_spec["recursive"] = {"type": "bool"}
    argument_spec["state"] = {
        "type": "str",
        "choices": ["absent", "create_temporary", "move", "present"],
        "default": "present",
    }
    argument_spec["suffix"] = {"type": "str"}
    argument_spec["vm"] = {"required": True, "type": "str"}

    return argument_spec


async def main():
    required_if = list([])

    module_args = prepare_argument_spec()
    module = AnsibleModule(
        argument_spec=module_args, required_if=required_if, supports_check_mode=True
    )
    if not module.params["vcenter_hostname"]:
        module.fail_json("vcenter_hostname cannot be empty")
    if not module.params["vcenter_username"]:
        module.fail_json("vcenter_username cannot be empty")
    if not module.params["vcenter_password"]:
        module.fail_json("vcenter_password cannot be empty")
    try:
        session = await open_session(
            vcenter_hostname=module.params["vcenter_hostname"],
            vcenter_username=module.params["vcenter_username"],
            vcenter_password=module.params["vcenter_password"],
            validate_certs=module.params["vcenter_validate_certs"],
            log_file=module.params["vcenter_rest_log_file"],
        )
    except EmbeddedModuleFailure as err:
        module.fail_json(err.get_message())
    result = await entry_point(module, session)
    module.exit_json(**result)


# template: default_module.j2
def build_url(params):
    return (
        "https://{vcenter_hostname}"
        "/api/vcenter/vm/{vm}/guest/filesystem/directories?action=create"
    ).format(**params)


async def entry_point(module, session):

    if module.params["state"] == "present":
        if "_create" in globals():
            operation = "create"
        else:
            operation = "update"
    elif module.params["state"] == "absent":
        operation = "delete"
    else:
        operation = module.params["state"]

    func = globals()["_" + operation]

    return await func(module.params, session)


async def _create(params, session):

    uniquity_keys = []

    payload = prepare_payload(params, PAYLOAD_FORMAT["create"])
    _url = (
        "https://{vcenter_hostname}"
        "/api/vcenter/vm/{vm}/guest/filesystem/directories?action=create"
    ).format(**params)
    async with session.post(_url, json=payload, **session_timeout(params)) as resp:
        if resp.status == 500:
            text = await resp.text()
            raise EmbeddedModuleFailure(
                f"Request has failed: status={resp.status}, {text}"
            )
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}

        if (resp.status in [200, 201]) and "error" not in _json:
            if isinstance(_json, str):  # 7.0.2 and greater
                _id = _json  # TODO: fetch the object
            elif isinstance(_json, dict) and "value" not in _json:
                _id = list(_json["value"].values())[0]
            elif isinstance(_json, dict) and "value" in _json:
                _id = _json["value"]
            _json_device_info = await get_device_info(session, _url, _id)
            if _json_device_info:
                _json = _json_device_info

        return await update_changed_flag(_json, resp.status, "create")


async def _create_temporary(params, session):
    _in_query_parameters = PAYLOAD_FORMAT["create_temporary"]["query"].keys()
    payload = prepare_payload(params, PAYLOAD_FORMAT["create_temporary"])
    subdevice_type = get_subdevice_type(
        "/api/vcenter/vm/{vm}/guest/filesystem/directories?action=createTemporary"
    )
    if subdevice_type and not params[subdevice_type]:
        _json = await exists(params, session, build_url(params))
        if _json:
            params[subdevice_type] = _json["id"]
    _url = (
        "https://{vcenter_hostname}"
        # aa
        "/api/vcenter/vm/{vm}/guest/filesystem/directories?action=createTemporary"
    ).format(**params) + gen_args(params, _in_query_parameters)
    async with session.post(_url, json=payload, **session_timeout(params)) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        if "value" not in _json:  # 7.0.2
            _json = {"value": _json}

        return await update_changed_flag(_json, resp.status, "create_temporary")


async def _delete(params, session):
    _in_query_parameters = PAYLOAD_FORMAT["delete"]["query"].keys()
    payload = prepare_payload(params, PAYLOAD_FORMAT["delete"])
    subdevice_type = get_subdevice_type(
        "/api/vcenter/vm/{vm}/guest/filesystem/directories?action=delete"
    )
    if subdevice_type and not params[subdevice_type]:
        _json = await exists(params, session, build_url(params))
        if _json:
            params[subdevice_type] = _json["id"]
    _url = (
        "https://{vcenter_hostname}"
        "/api/vcenter/vm/{vm}/guest/filesystem/directories?action=delete"
    ).format(**params) + gen_args(params, _in_query_parameters)
    async with session.post(_url, json=payload, **session_timeout(params)) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        return await update_changed_flag(_json, resp.status, "delete")


async def _move(params, session):
    _in_query_parameters = PAYLOAD_FORMAT["move"]["query"].keys()
    payload = prepare_payload(params, PAYLOAD_FORMAT["move"])
    subdevice_type = get_subdevice_type(
        "/api/vcenter/vm/{vm}/guest/filesystem/directories?action=move"
    )
    if subdevice_type and not params[subdevice_type]:
        _json = await exists(params, session, build_url(params))
        if _json:
            params[subdevice_type] = _json["id"]
    _url = (
        "https://{vcenter_hostname}"
        # aa
        "/api/vcenter/vm/{vm}/guest/filesystem/directories?action=move"
    ).format(**params) + gen_args(params, _in_query_parameters)
    async with session.post(_url, json=payload, **session_timeout(params)) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        if "value" not in _json:  # 7.0.2
            _json = {"value": _json}

        return await update_changed_flag(_json, resp.status, "move")


if __name__ == "__main__":
    import asyncio

    current_loop = asyncio.get_event_loop_policy().get_event_loop()
    current_loop.run_until_complete(main())
