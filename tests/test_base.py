import pytest
import requests_mock
import unittest
import time

from badfish import main
from tests import config


def no_sleep(_):
    pass


class TestBase(unittest.TestCase):
    time.sleep = no_sleep
    first_call = True
    last_on = False

    def jobs_callback(self, request, context):
        if self.first_call:
            return {}
        else:
            self.first_call = False
            return {"JobID": config.JOB_ID}

    def state_callback(self, request, context):
        if self.last_on:
            self.last_on = False
            return {u"PowerState": "Off"}
        else:
            self.last_on = True
            return {u"PowerState": "On"}

    @pytest.fixture(autouse=True)
    def inject_capsys(self, capsys):
        self._capsys = capsys

    @requests_mock.mock()
    def badfish_call(self, _mock):
        _mock.get("https://%s/redfish/v1/Systems/System.Embedded.1/Bios" % config.MOCK_HOST,
                  json={"Attributes": {"BootMode": u"Bios"}}
                  )
        _mock.get("https://%s/redfish/v1/Systems/System.Embedded.1/BootSources" % config.MOCK_HOST,
                  json={"Attributes": {"BootSeq": self.boot_seq}})
        _mock.get("https://%s/redfish/v1/Managers/iDRAC.Embedded.1/Jobs" % config.MOCK_HOST,
                  json=self.jobs_callback)
        _mock.post("https://%s/redfish/v1/Managers/iDRAC.Embedded.1/Jobs" % config.MOCK_HOST,
                   json={"JobID": config.JOB_ID})
        _mock.delete("https://%s/redfish/v1/Managers/iDRAC.Embedded.1/Jobs/%s" % (config.MOCK_HOST, config.JOB_ID),
                     json={"JobID": config.JOB_ID})
        _mock.get("https://%s/redfish/v1/Managers/iDRAC.Embedded.1/Jobs/%s" % (config.MOCK_HOST, config.JOB_ID),
                  json={u"Message": "Task successfully scheduled."})
        _mock.patch("https://%s/redfish/v1/Systems/System.Embedded.1/Bios/Settings" % config.MOCK_HOST,
                    json={})
        _mock.post("https://%s/redfish/v1/Managers/iDRAC.Embedded.1/Actions/Manager.Reset/" % config.MOCK_HOST,
                   json={}, status_code=204)
        _mock.post("https://%s/redfish/v1/Systems/System.Embedded.1/Actions/ComputerSystem.Reset" % config.MOCK_HOST,
                   json={}, status_code=204)
        _mock.get("https://%s/redfish/v1/Systems/System.Embedded.1/" % config.MOCK_HOST,
                  json=self.state_callback)
        argv = ["-H", config.MOCK_HOST, "-u", config.MOCK_USER, "-p", config.MOCK_PASS]
        argv.extend(self.args)
        main(argv)
        out, err = self._capsys.readouterr()
        return err
