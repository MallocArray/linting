#!/usr/bin/python

# (c) 2020-2022, NetApp, Inc
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

'''
na_ontap_login_messages
'''

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
module: na_ontap_login_messages
author: NetApp Ansible Team (@carchi8py) <ng-ansibleteam@netapp.com>
extends_documentation_fragment:
    - netapp.ontap.netapp.na_ontap
version_added: '20.1.0'
short_description: Setup login banner and message of the day
description:
    - This module allows you to manipulate login banner and motd for a vserver
options:
    banner:
        description:
        - Login banner Text message.
        type: str
    vserver:
        description:
        - The name of the SVM login messages should be set for.
        - With ZAPI, this option is required.  This a cluster or data SVM.
        - With REST, this is a data SVM.
        - With REST, cluster scope is assumed when this option is absent.
        type: str
    motd_message:
        description:
        - MOTD Text message.
        type: str
        aliases:
          - message
    show_cluster_motd:
        description:
        - Set to I(false) if Cluster-level Message of the Day should not be shown
        type: bool
        default: True
'''

EXAMPLES = """

    - name: modify banner vserver
      netapp.ontap.na_ontap_login_messages:
        vserver: trident_svm
        banner: this is trident vserver
        username: "{{ username }}"
        password: "{{ password }}"
        hostname: "{{ hostname }}"

    - name: modify motd vserver
      netapp.ontap.na_ontap_login_messages:
        vserver: trident_svm
        motd_message: this is trident vserver
        show_cluster_motd: True
        username: "{{ username }}"
        password: "{{ password }}"
        hostname: "{{ hostname }}"

    - name: modify motd cluster - REST
      netapp.ontap.na_ontap_login_messages:
        motd_message: this is a cluster motd with REST
        show_cluster_motd: True
        username: "{{ username }}"
        password: "{{ password }}"
        hostname: "{{ hostname }}"

"""

RETURN = """

"""

import traceback
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native
import ansible_collections.netapp.ontap.plugins.module_utils.netapp as netapp_utils
from ansible_collections.netapp.ontap.plugins.module_utils.netapp_module import NetAppModule
from ansible_collections.netapp.ontap.plugins.module_utils.netapp import OntapRestAPI
from ansible_collections.netapp.ontap.plugins.module_utils import rest_generic
from ansible_collections.netapp.ontap.plugins.module_utils import rest_vserver

HAS_NETAPP_LIB = netapp_utils.has_netapp_lib()


class NetAppOntapLoginMessages:
    """
    modify and delete login banner and motd
    """

    def __init__(self):
        self.use_rest = False
        self.argument_spec = netapp_utils.na_ontap_host_argument_spec()
        self.argument_spec.update(dict(
            vserver=dict(type='str'),
            banner=dict(type='str'),
            motd_message=dict(type='str', aliases=['message']),
            show_cluster_motd=dict(default=True, type='bool')
        ))

        self.module = AnsibleModule(
            argument_spec=self.argument_spec,
            supports_check_mode=True,
            required_one_of=[['show_cluster_motd', 'banner', 'motd_message']]
        )

        self.na_helper = NetAppModule()
        self.parameters = self.na_helper.set_parameters(self.module.params)

        self.rest_api = OntapRestAPI(self.module)
        if self.rest_api.is_rest():
            self.use_rest = True
        else:
            if not netapp_utils.has_netapp_lib():
                self.module.fail_json(msg=netapp_utils.netapp_lib_is_required())
            if not self.parameters.get('vserver'):
                self.module.fail_json(msg="Error: vserver is a required parameter when using ZAPI.")
            self.server = netapp_utils.setup_na_ontap_zapi(module=self.module, vserver=self.parameters['vserver'])

    def get_banner_motd(self):
        if self.use_rest:
            api = 'security/login/messages'
            query = {
                'fields': 'banner,message,show_cluster_message,uuid',
                'scope': 'cluster'
            }
            vserver = self.parameters.get('vserver')
            if vserver:
                query['scope'] = 'svm'
                query['svm.name'] = vserver

            record, error = rest_generic.get_one_record(self.rest_api, api, query)
            if error:
                self.module.fail_json(msg='Error fetching login_banner info: %s' % error)
            if record is None and vserver is None:
                self.module.fail_json(msg='Error fetching login_banner info for cluster - no data.')
            return_result = {
                'banner': record['banner'].rstrip() if record and record.get('banner') else '',
                'motd_message': record['message'].rstrip() if record and record.get('message') else '',
                # we need the SVM UUID to add banner or motd if they are not present
                'uuid': record['uuid'] if record else self.get_svm_uuid(vserver),
            }
            if record and record.get('show_cluster_message') is not None:
                return_result['show_cluster_motd'] = record['show_cluster_message']
            return return_result

        # ZAPI
        motd, show_cluster_motd = self.get_motd_zapi()
        return {
            'banner': self.get_login_banner_zapi(),
            'motd_message': motd,
            'show_cluster_motd': show_cluster_motd
        }

    def get_login_banner_zapi(self):
        login_banner_get_iter = netapp_utils.zapi.NaElement('vserver-login-banner-get-iter')
        query = netapp_utils.zapi.NaElement('query')
        login_banner_info = netapp_utils.zapi.NaElement('vserver-login-banner-info')
        login_banner_info.add_new_child('vserver', self.parameters['vserver'])
        query.add_child_elem(login_banner_info)
        login_banner_get_iter.add_child_elem(query)
        try:
            result = self.server.invoke_successfully(login_banner_get_iter, enable_tunneling=True)
        except netapp_utils.zapi.NaApiError as error:
            self.module.fail_json(msg='Error fetching login_banner info: %s' % to_native(error),
                                  exception=traceback.format_exc())
        if result.get_child_by_name('num-records') and int(result.get_child_content('num-records')) > 0:
            login_banner_info = result.get_child_by_name('attributes-list').get_child_by_name(
                'vserver-login-banner-info')
            banner = login_banner_info.get_child_content('message')
            banner = str(banner).rstrip()
            # if the message is '-' that means the banner doesn't exist.
            if banner in ('-', 'None'):
                banner = ''
            return banner
        return None

    def get_motd_zapi(self):
        motd_get_iter = netapp_utils.zapi.NaElement('vserver-motd-get-iter')
        query = netapp_utils.zapi.NaElement('query')
        motd_info = netapp_utils.zapi.NaElement('vserver-motd-info')
        motd_info.add_new_child('vserver', self.parameters['vserver'])
        query.add_child_elem(motd_info)
        motd_get_iter.add_child_elem(query)
        try:
            result = self.server.invoke_successfully(motd_get_iter, enable_tunneling=True)
        except netapp_utils.zapi.NaApiError as error:
            self.module.fail_json(msg='Error fetching motd info: %s' % to_native(error),
                                  exception=traceback.format_exc())
        if result.get_child_by_name('num-records') and \
                int(result.get_child_content('num-records')) > 0:
            motd_info = result.get_child_by_name('attributes-list').get_child_by_name(
                'vserver-motd-info')
            motd_message = motd_info.get_child_content('message')
            motd_message = str(motd_message).rstrip()
            if motd_message == 'None':
                motd_message = ''
            show_cluster_motd = motd_info.get_child_content('is-cluster-message-enabled') == 'true'
            return motd_message, show_cluster_motd
        return '', False

    def modify_rest(self, modify, uuid):
        api = 'security/login/messages'
        body = {
        }
        if 'banner' in modify:
            body['banner'] = modify['banner']
        if 'motd_message' in modify:
            body['message'] = modify['motd_message']
        if modify.get('show_cluster_motd') is not None:
            body['show_cluster_message'] = modify['show_cluster_motd']
        if body:
            dummy, error = rest_generic.patch_async(self.rest_api, api, uuid, body)
            if error:
                keys = list(body.keys())
                self.module.fail_json(msg='Error modifying %s: %s' % (', '.join(keys), error))

    def modify_banner(self, modify):
        login_banner_modify = netapp_utils.zapi.NaElement('vserver-login-banner-modify-iter')
        login_banner_modify.add_new_child('message', modify['banner'])
        query = netapp_utils.zapi.NaElement('query')
        login_banner_info = netapp_utils.zapi.NaElement('vserver-login-banner-info')
        login_banner_info.add_new_child('vserver', self.parameters['vserver'])
        query.add_child_elem(login_banner_info)
        login_banner_modify.add_child_elem(query)
        try:
            self.server.invoke_successfully(login_banner_modify, enable_tunneling=False)
        except netapp_utils.zapi.NaApiError as err:
            self.module.fail_json(msg="Error modifying login_banner: %s" % (to_native(err)),
                                  exception=traceback.format_exc())

    def modify_motd(self, modify):
        motd_create = netapp_utils.zapi.NaElement('vserver-motd-modify-iter')
        if modify.get('motd_message') is not None:
            motd_create.add_new_child('message', modify['motd_message'])
        if modify.get('show_cluster_motd') is not None:
            motd_create.add_new_child('is-cluster-message-enabled', 'true' if modify['show_cluster_motd'] is True else 'false')
        query = netapp_utils.zapi.NaElement('query')
        motd_info = netapp_utils.zapi.NaElement('vserver-motd-info')
        motd_info.add_new_child('vserver', self.parameters['vserver'])
        query.add_child_elem(motd_info)
        motd_create.add_child_elem(query)
        try:
            self.server.invoke_successfully(motd_create, enable_tunneling=False)
        except netapp_utils.zapi.NaApiError as err:
            self.module.fail_json(msg="Error modifying motd: %s" % (to_native(err)),
                                  exception=traceback.format_exc())

    def get_svm_uuid(self, vserver):
        """
        Get a svm's uuid
        :return: uuid of the svm
        """
        uuid, error = rest_vserver.get_vserver_uuid(self.rest_api, vserver)
        if error is not None:
            self.module.fail_json(msg="Error fetching vserver %s: %s" % (vserver, error))
        if uuid is None:
            self.module.fail_json(msg="Error fetching vserver %s. Please make sure vserver name is correct. For cluster vserver, don't set vserver."
                                  % vserver)
        return uuid

    def apply(self):
        if not self.use_rest:
            netapp_utils.ems_log_event("na_ontap_login_banner", self.server)

        current = self.get_banner_motd()
        modify = self.na_helper.get_modified_attributes(current, self.parameters)
        if self.na_helper.changed and not self.module.check_mode:
            if self.use_rest:
                self.modify_rest(modify, current['uuid'])
            else:
                if modify.get('banner') is not None:
                    self.modify_banner(modify)
                if modify.get('show_cluster_motd') is not None or modify.get('motd_message') is not None:
                    self.modify_motd(modify)

        self.module.exit_json(changed=self.na_helper.changed)


def main():
    '''Execute action from playbook'''
    messages_obj = NetAppOntapLoginMessages()
    messages_obj.apply()


if __name__ == '__main__':
    main()
