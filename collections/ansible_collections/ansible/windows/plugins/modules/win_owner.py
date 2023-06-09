#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2015, Hans-Joachim Kliemeck <git@kliemeck.de>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r'''
---
module: win_owner
short_description: Set owner
description:
    - Set owner of files or directories.
options:
  path:
    description:
      - Path to be used for changing owner.
    type: path
    required: yes
  user:
    description:
      - Name to be used for changing owner.
    type: str
    required: yes
  recurse:
    description:
      - Indicates if the owner should be changed recursively.
    type: bool
    default: no
seealso:
- module: ansible.windows.win_acl
- module: ansible.windows.win_file
- module: ansible.windows.win_stat
author:
- Hans-Joachim Kliemeck (@h0nIg)
'''

EXAMPLES = r'''
- name: Change owner of path
  ansible.windows.win_owner:
    path: C:\apache
    user: apache
    recurse: true

- name: Set the owner of root directory
  ansible.windows.win_owner:
    path: C:\apache
    user: SYSTEM
    recurse: false
'''

RETURN = r'''

'''
