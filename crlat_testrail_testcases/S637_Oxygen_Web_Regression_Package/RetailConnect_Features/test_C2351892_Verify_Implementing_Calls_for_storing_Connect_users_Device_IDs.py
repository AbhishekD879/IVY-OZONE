import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.retail
@vtest
class Test_C2351892_Verify_Implementing_Calls_for_storing_Connect_users_Device_IDs(Common):
    """
    TR_ID: C2351892
    NAME: Verify Implementing Calls for storing Connect users Device IDs
    DESCRIPTION: This test case verifies the positive scenario of implementing calls for storing, getting, and deleting Connect users Device IDs
    PRECONDITIONS: To see what optin link is in use, type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: Links for dev0 environment:
    PRECONDITIONS: https://optin-dev0.coralsports.dev.cloud.ladbrokescoral.com/api/connect/save?deviceId={device Id value}
    PRECONDITIONS: https://optin-dev0.coralsports.dev.cloud.ladbrokescoral.com/api/connect/get?deviceId={device Id value}
    PRECONDITIONS: https://optin-dev0.coralsports.dev.cloud.ladbrokescoral.com/api/connect/remove?deviceId={device Id value}
    PRECONDITIONS: The same device Id should be used for each stet in one test flow
    PRECONDITIONS: The example of test device id: dssljlk689298734knkdlflls-dfsduw74njn38
    """
    keep_browser_open = True

    def test_001_save_device_idgo_to_httpsoptin_dev0coralsportsdevcloudladbrokescoralcomapiconnectsavedeviceiddevice_id_value(self):
        """
        DESCRIPTION: Save device id:
        DESCRIPTION: go to https://optin-dev0.coralsports.dev.cloud.ladbrokescoral.com/api/connect/save?deviceId={device Id value}
        EXPECTED: The system returns  { "status": "ok" }
        """
        pass

    def test_002_get_device_idgo_to_httpsoptin_dev0coralsportsdevcloudladbrokescoralcomapiconnectgetdeviceiddevice_id_value(self):
        """
        DESCRIPTION: Get device id:
        DESCRIPTION: go to https://optin-dev0.coralsports.dev.cloud.ladbrokescoral.com/api/connect/get?deviceId={device Id value}
        EXPECTED: The system returns  { "status": "ok", ''id'': ''{device Id value}'' ''exists'': ''true''}
        """
        pass

    def test_003_delete_device_idhttpsoptin_dev0coralsportsdevcloudladbrokescoralcomapiconnectremovedeviceiddevice_id_value(self):
        """
        DESCRIPTION: Delete device id:
        DESCRIPTION: https://optin-dev0.coralsports.dev.cloud.ladbrokescoral.com/api/connect/remove?deviceId={device Id value}
        EXPECTED: The system returns  { "status": "ok", ''id'': ''{device Id value}''}
        """
        pass

    def test_004_get_device_id_to_check_the_device_id_has_been_really_deletedgo_to_httpsoptin_dev0coralsportsdevcloudladbrokescoralcomapiconnectgetdeviceiddevice_id_value(self):
        """
        DESCRIPTION: Get device id to check the device id has been really deleted:
        DESCRIPTION: go to https://optin-dev0.coralsports.dev.cloud.ladbrokescoral.com/api/connect/get?deviceId={device Id value}
        EXPECTED: The system returns  { "status": "ERROR", message: ''Can't find device by id: {device Id value}",  ''id'': ''{device Id value}''}
        """
        pass
