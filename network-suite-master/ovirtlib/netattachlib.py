# Copyright 2019 Red Hat, Inc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA
#
# Refer to the README and COPYING files for full details of the license

from ovirtsdk4 import types


class IpVersion(object):

    V4 = types.IpVersion.V4
    V6 = types.IpVersion.V6


DYNAMIC_IP_CONFIG = [
    types.IpAddressAssignment(assignment_method=types.BootProtocol.DHCP),
    types.IpAddressAssignment(assignment_method=types.BootProtocol.DHCP,
                              ip=types.Ip(version=IpVersion.V6))
]


class IpAssignment(object):

    def __init__(self, addr, mask, gateway=None, version=IpVersion.V4,
                 boot_protocol=None):
        self._ip = types.Ip(addr, gateway, mask, version)
        self._boot_protocol = boot_protocol

    @property
    def address(self):
        return self._ip.address

    @property
    def netmask(self):
        return self._ip.netmask

    @property
    def gateway(self):
        return self._ip.gateway

    @property
    def version(self):
        return self._ip.version

    @property
    def boot_protocol(self):
        return self._boot_protocol


class StaticIpAssignment(IpAssignment):

    def __init__(self, addr, mask, gateway=None, version=IpVersion.V4):
        super(StaticIpAssignment, self).__init__(addr, mask, gateway, version,
                                                 types.BootProtocol.STATIC)


class NetworkAttachmentData(object):

    def __init__(self, network, nic_name, ip_assignments=()):
        self._network = network
        self._nic_name = nic_name
        self._ip_assignments = ip_assignments

    @property
    def network(self):
        return self._network

    @property
    def nic_name(self):
        return self._nic_name

    @property
    def ip_assignments(self):
        return self._ip_assignments

    def to_network_attachment(self):
        """
        :param attachment_data: netattachlib.NetworkAttachmentData
        :return: types.NetworkAttachment
        """
        attachment = types.NetworkAttachment(
            network=self.network.get_sdk_type(),
            host_nic=types.HostNic(name=self.nic_name)
        )
        attachment.ip_address_assignments = self._to_ip_address_assignments(
            self.ip_assignments
        )
        return attachment

    def _to_ip_address_assignments(self, ip_assignments):
        """
        :param ip_assignments: list(netattachlib.IpAssignment)
        :return: list(types.IpAddressAssignment)
        """
        return [
            self._to_ip_address_assignment(ip_assignment)
            for ip_assignment in ip_assignments
        ]

    def _to_ip_address_assignment(self, ip_assignment):
        """
        :param ip_assignment: netattachlib.IpAssignment
        :return: types.IpAddressAssignment
        """
        ip_address_assignment = types.IpAddressAssignment(
            assignment_method=ip_assignment.boot_protocol,
            ip=types.Ip(
                address=ip_assignment.address,
                netmask=ip_assignment.netmask,
                gateway=ip_assignment.gateway,
                version=ip_assignment.version
            )
        )
        return ip_address_assignment
