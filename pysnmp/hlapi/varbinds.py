#
# This file is part of pysnmp software.
#
# Copyright (c) 2005-2019, Ilya Etingof <etingof@gmail.com>
# License: https://www.pysnmp.com/pysnmp/license.html
#
from pysnmp.smi import view
from pysnmp.smi.rfc1902 import *

__all__ = ['CommandGeneratorVarBinds', 'NotificationOriginatorVarBinds']


class AbstractVarBinds:
    @staticmethod
    def getMibViewController(snmpEngine):
        mibViewController = snmpEngine.getUserContext('mibViewController')
        if not mibViewController:
            mibViewController = view.MibViewController(
                snmpEngine.getMibBuilder()
            )
            snmpEngine.setUserContext(mibViewController=mibViewController)
        return mibViewController


class CommandGeneratorVarBinds(AbstractVarBinds):
    def makeVarBinds(self, snmpEngine, varBinds):
        mibViewController = self.getMibViewController(snmpEngine)
        __varBinds = []
        for varBind in varBinds:
            if isinstance(varBind, ObjectType):
                pass
            elif isinstance(varBind[0], ObjectIdentity):
                varBind = ObjectType(*varBind)
            elif isinstance(varBind[0][0], tuple):  # legacy
                varBind = ObjectType(ObjectIdentity(varBind[0][0][0], varBind[0][0][1], *varBind[0][1:]), varBind[1])
            else:
                varBind = ObjectType(ObjectIdentity(varBind[0]), varBind[1])

            __varBinds.append(varBind.resolveWithMib(mibViewController, ignoreErrors=False))

        return __varBinds

    def unmakeVarBinds(self, snmpEngine, varBinds, lookupMib=True):
        if lookupMib:
            mibViewController = self.getMibViewController(snmpEngine)
            varBinds = [ObjectType(ObjectIdentity(x[0]), x[1]).resolveWithMib(
                mibViewController) for x in varBinds]

        return varBinds


class NotificationOriginatorVarBinds(AbstractVarBinds):
    def makeVarBinds(self, snmpEngine, varBinds):
        mibViewController = self.getMibViewController(snmpEngine)
        if isinstance(varBinds, NotificationType):
            varBinds.resolveWithMib(
                mibViewController, ignoreErrors=False)
        __varBinds = []
        for varBind in varBinds:
            if isinstance(varBind, ObjectType):
                pass
            elif isinstance(varBind[0], ObjectIdentity):
                varBind = ObjectType(*varBind)
            else:
                varBind = ObjectType(ObjectIdentity(varBind[0]), varBind[1])
            __varBinds.append(varBind.resolveWithMib(
                mibViewController, ignoreErrors=False))
        return __varBinds

    def unmakeVarBinds(self, snmpEngine, varBinds, lookupMib=False):
        if lookupMib:
            mibViewController = self.getMibViewController(snmpEngine)
            varBinds = [ObjectType(ObjectIdentity(x[0]), x[1]).resolveWithMib(
                mibViewController) for x in varBinds]
        return varBinds
