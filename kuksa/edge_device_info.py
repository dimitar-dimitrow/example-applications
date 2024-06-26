# Copyright (c) 2024 Contributors to the Eclipse Foundation
#
# See the NOTICE file(s) distributed with this work for additional
# information regarding copyright ownership.
#
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License 2.0 which is available at
# https://www.eclipse.org/legal/epl-2.0, or the Apache License, Version 2.0
# which is available at https://www.apache.org/licenses/LICENSE-2.0.
#
# SPDX-License-IDentifier: EPL-2.0 OR Apache-2.0

import json
import logging

from ditto.model.namespaced_id import NamespacedID

DEVICE_ID_KEY = "deviceId"
TENANT_ID_KEY = "tenantId"
POLICY_ID_KEY = "policyId"

ALLOWED_KEYS = [DEVICE_ID_KEY, TENANT_ID_KEY, POLICY_ID_KEY]


class EdgeDeviceInfo:
    def __init__(self, **kwargs):
        self.deviceId = None
        self.tenantId = None
        self.policyId = None
        self.log = logging.getLogger('EDGE_DEVICE')

        for k, v in kwargs.items():
            if k in ALLOWED_KEYS:
                self.__setattr__(k, v)

    def unmarshal_json(self, data: json):
        try:
            envelope_dict = json.loads(data)
        except json.JSONDecodeError as jex:
            return jex

        for k, v in envelope_dict.copy().items():
            if k == DEVICE_ID_KEY:
                self.deviceId = NamespacedID().from_string(v)

            if k == POLICY_ID_KEY:
                self.policyId = NamespacedID().from_string(v)

            if k == TENANT_ID_KEY:
                self.tenantId = v

        self.log.info(f'Device info - {envelope_dict}')
        return 0