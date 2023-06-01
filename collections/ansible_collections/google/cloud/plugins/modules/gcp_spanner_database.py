#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2017 Google
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# ----------------------------------------------------------------------------
#
#     ***     AUTO GENERATED CODE    ***    Type: MMv1     ***
#
# ----------------------------------------------------------------------------
#
#     This file is automatically generated by Magic Modules and manual
#     changes will be clobbered when the file is regenerated.
#
#     Please read more about how to change this file at
#     https://www.github.com/GoogleCloudPlatform/magic-modules
#
# ----------------------------------------------------------------------------

from __future__ import absolute_import, division, print_function

__metaclass__ = type

################################################################################
# Documentation
################################################################################

ANSIBLE_METADATA = {'metadata_version': '1.1', 'status': ["preview"], 'supported_by': 'community'}

DOCUMENTATION = '''
---
module: gcp_spanner_database
description:
- A Cloud Spanner Database which is hosted on a Spanner instance.
short_description: Creates a GCP Database
author: Google Inc. (@googlecloudplatform)
requirements:
- python >= 2.6
- requests >= 2.18.4
- google-auth >= 1.3.0
options:
  state:
    description:
    - Whether the given object should exist in GCP
    choices:
    - present
    - absent
    default: present
    type: str
  name:
    description:
    - A unique identifier for the database, which cannot be changed after the instance
      is created. Values are of the form [a-z][-a-z0-9]*[a-z0-9].
    required: true
    type: str
  extra_statements:
    description:
    - 'An optional list of DDL statements to run inside the newly created database.
      Statements can create tables, indexes, etc. These statements execute atomically
      with the creation of the database: if there is an error in any statement, the
      database is not created.'
    elements: str
    required: false
    type: list
  encryption_config:
    description:
    - Encryption configuration for the database .
    required: false
    type: dict
    suboptions:
      kms_key_name:
        description:
        - Fully qualified name of the KMS key to use to encrypt this database. This
          key must exist in the same location as the Spanner Database.
        required: true
        type: str
  instance:
    description:
    - The instance to create the database on.
    - 'This field represents a link to a Instance resource in GCP. It can be specified
      in two ways. First, you can place a dictionary with key ''name'' and value of
      your resource''s name Alternatively, you can add `register: name-of-resource`
      to a gcp_spanner_instance task and then set this instance field to "{{ name-of-resource
      }}"'
    required: true
    type: dict
  project:
    description:
    - The Google Cloud Platform project to use.
    type: str
  auth_kind:
    description:
    - The type of credential used.
    type: str
    required: true
    choices:
    - application
    - machineaccount
    - serviceaccount
  service_account_contents:
    description:
    - The contents of a Service Account JSON file, either in a dictionary or as a
      JSON string that represents it.
    type: jsonarg
  service_account_file:
    description:
    - The path of a Service Account JSON file if serviceaccount is selected as type.
    type: path
  service_account_email:
    description:
    - An optional service account email address if machineaccount is selected and
      the user does not wish to use the default email.
    type: str
  scopes:
    description:
    - Array of scopes to be used
    type: list
    elements: str
  env_type:
    description:
    - Specifies which Ansible environment you're running this module within.
    - This should not be set unless you know what you're doing.
    - This only alters the User Agent string for any API requests.
    type: str
notes:
- 'API Reference: U(https://cloud.google.com/spanner/docs/reference/rest/v1/projects.instances.databases)'
- 'Official Documentation: U(https://cloud.google.com/spanner/)'
- for authentication, you can set service_account_file using the C(GCP_SERVICE_ACCOUNT_FILE)
  env variable.
- for authentication, you can set service_account_contents using the C(GCP_SERVICE_ACCOUNT_CONTENTS)
  env variable.
- For authentication, you can set service_account_email using the C(GCP_SERVICE_ACCOUNT_EMAIL)
  env variable.
- For authentication, you can set auth_kind using the C(GCP_AUTH_KIND) env variable.
- For authentication, you can set scopes using the C(GCP_SCOPES) env variable.
- Environment variables values will only be used if the playbook values are not set.
- The I(service_account_email) and I(service_account_file) options are mutually exclusive.
'''

EXAMPLES = '''
- name: create a instance
  google.cloud.gcp_spanner_instance:
    name: instance-database
    display_name: My Spanner Instance
    node_count: 2
    labels:
      cost_center: ti-1700004
    config: regional-us-central1
    project: "{{ gcp_project }}"
    auth_kind: "{{ gcp_cred_kind }}"
    service_account_file: "{{ gcp_cred_file }}"
    state: present
  register: instance

- name: create a database
  google.cloud.gcp_spanner_database:
    name: webstore
    instance: "{{ instance }}"
    project: test_project
    auth_kind: serviceaccount
    service_account_file: "/tmp/auth.pem"
    state: present
'''

RETURN = '''
name:
  description:
  - A unique identifier for the database, which cannot be changed after the instance
    is created. Values are of the form [a-z][-a-z0-9]*[a-z0-9].
  returned: success
  type: str
extraStatements:
  description:
  - 'An optional list of DDL statements to run inside the newly created database.
    Statements can create tables, indexes, etc. These statements execute atomically
    with the creation of the database: if there is an error in any statement, the
    database is not created.'
  returned: success
  type: list
encryptionConfig:
  description:
  - Encryption configuration for the database .
  returned: success
  type: complex
  contains:
    kmsKeyName:
      description:
      - Fully qualified name of the KMS key to use to encrypt this database. This
        key must exist in the same location as the Spanner Database.
      returned: success
      type: str
instance:
  description:
  - The instance to create the database on.
  returned: success
  type: dict
'''

################################################################################
# Imports
################################################################################

from ansible_collections.google.cloud.plugins.module_utils.gcp_utils import (
    navigate_hash,
    GcpSession,
    GcpModule,
    GcpRequest,
    remove_nones_from_dict,
    replace_resource_dict,
)
import json
import time

################################################################################
# Main
################################################################################


def main():
    """Main function"""

    module = GcpModule(
        argument_spec=dict(
            state=dict(default='present', choices=['present', 'absent'], type='str'),
            name=dict(required=True, type='str'),
            extra_statements=dict(type='list', elements='str'),
            encryption_config=dict(type='dict', options=dict(kms_key_name=dict(required=True, type='str'))),
            instance=dict(required=True, type='dict'),
        )
    )

    if not module.params['scopes']:
        module.params['scopes'] = ['https://www.googleapis.com/auth/spanner.admin']

    state = module.params['state']

    fetch = fetch_resource(module, self_link(module))
    changed = False

    if 'instance' in module.params and 'name' in module.params['instance']:
        module.params['instance']['name'] = module.params['instance']['name'].split('/')[-1]

    if fetch:
        if state == 'present':
            if is_different(module, fetch):
                update(module, self_link(module), fetch)
                fetch = fetch_resource(module, self_link(module))
                changed = True
        else:
            delete(module, self_link(module))
            fetch = {}
            changed = True
    else:
        if state == 'present':
            fetch = create(module, collection(module))
            changed = True
        else:
            fetch = {}

    fetch.update({'changed': changed})

    module.exit_json(**fetch)


def create(module, link):
    auth = GcpSession(module, 'spanner')
    return wait_for_operation(module, auth.post(link, resource_to_request(module)))


def update(module, link, fetch):
    module.fail_json(msg="Spanner objects can't be updated to ensure data safety")


def update_fields(module, request, response):
    if response.get('extraStatements') != request.get('extraStatements'):
        extra_statements_update(module, request, response)


def extra_statements_update(module, request, response):
    auth = GcpSession(module, 'spanner')
    auth.patch(
        ''.join(["https://spanner.googleapis.com/v1/", "projects/{project}/instances/{instance}/databases/{name}/ddl"]).format(**module.params),
        {u'extraStatements': module.params.get('extra_statements')},
    )


def delete(module, link):
    auth = GcpSession(module, 'spanner')
    return return_if_object(module, auth.delete(link))


def resource_to_request(module):
    request = {
        u'name': module.params.get('name'),
        u'extraStatements': module.params.get('extra_statements'),
        u'encryptionConfig': DatabaseEncryptionconfig(module.params.get('encryption_config', {}), module).to_request(),
    }
    request = encode_request(request, module)
    return_vals = {}
    for k, v in request.items():
        if v or v is False:
            return_vals[k] = v

    return return_vals


def fetch_resource(module, link, allow_not_found=True):
    auth = GcpSession(module, 'spanner')
    return return_if_object(module, auth.get(link), allow_not_found)


def self_link(module):
    res = {'project': module.params['project'], 'instance': replace_resource_dict(module.params['instance'], 'name'), 'name': module.params['name']}
    return "https://spanner.googleapis.com/v1/projects/{project}/instances/{instance}/databases/{name}".format(**res)


def collection(module):
    res = {'project': module.params['project'], 'instance': replace_resource_dict(module.params['instance'], 'name')}
    return "https://spanner.googleapis.com/v1/projects/{project}/instances/{instance}/databases".format(**res)


def return_if_object(module, response, allow_not_found=False):
    # If not found, return nothing.
    if allow_not_found and response.status_code == 404:
        return None

    # If no content, return nothing.
    if response.status_code == 204:
        return None

    try:
        module.raise_for_status(response)
        result = response.json()
    except getattr(json.decoder, 'JSONDecodeError', ValueError):
        module.fail_json(msg="Invalid JSON response with error: %s" % response.text)

    result = decode_response(result, module)

    if navigate_hash(result, ['error', 'errors']):
        module.fail_json(msg=navigate_hash(result, ['error', 'errors']))

    return result


def is_different(module, response):
    request = resource_to_request(module)
    response = response_to_hash(module, response)
    request = decode_response(request, module)

    # Remove all output-only from response.
    response_vals = {}
    for k, v in response.items():
        if k in request:
            response_vals[k] = v

    request_vals = {}
    for k, v in request.items():
        if k in response:
            request_vals[k] = v

    return GcpRequest(request_vals) != GcpRequest(response_vals)


# Remove unnecessary properties from the response.
# This is for doing comparisons with Ansible's current parameters.
def response_to_hash(module, response):
    return {
        u'name': module.params.get('name'),
        u'extraStatements': response.get(u'extraStatements'),
        u'encryptionConfig': DatabaseEncryptionconfig(response.get(u'encryptionConfig', {}), module).from_response(),
    }


def async_op_url(module, extra_data=None):
    if extra_data is None:
        extra_data = {}
    url = "https://spanner.googleapis.com/v1/{op_id}"
    combined = extra_data.copy()
    combined.update(module.params)
    return url.format(**combined)


def wait_for_operation(module, response):
    op_result = return_if_object(module, response)
    if op_result is None:
        return {}
    status = navigate_hash(op_result, ['done'])
    wait_done = wait_for_completion(status, op_result, module)
    raise_if_errors(wait_done, ['error'], module)
    return navigate_hash(wait_done, ['response'])


def wait_for_completion(status, op_result, module):
    op_id = navigate_hash(op_result, ['name'])
    op_uri = async_op_url(module, {'op_id': op_id})
    while not status:
        raise_if_errors(op_result, ['error'], module)
        time.sleep(1.0)
        op_result = fetch_resource(module, op_uri, False)
        status = navigate_hash(op_result, ['done'])
    return op_result


def raise_if_errors(response, err_path, module):
    errors = navigate_hash(response, err_path)
    if errors is not None:
        module.fail_json(msg=errors)


def decode_response(response, module):
    if not response:
        return response

    if 'name' not in response:
        return response

    if '/operations/' in response['name']:
        return response

    response['name'] = response['name'].split('/')[-1]
    return response


def encode_request(request, module):
    request['create_statement'] = "CREATE DATABASE `{0}`".format(module.params['name'])
    del request['name']
    return request


class DatabaseEncryptionconfig(object):
    def __init__(self, request, module):
        self.module = module
        if request:
            self.request = request
        else:
            self.request = {}

    def to_request(self):
        return remove_nones_from_dict({u'kmsKeyName': self.request.get('kms_key_name')})

    def from_response(self):
        return remove_nones_from_dict({u'kmsKeyName': self.request.get(u'kmsKeyName')})


if __name__ == '__main__':
    main()