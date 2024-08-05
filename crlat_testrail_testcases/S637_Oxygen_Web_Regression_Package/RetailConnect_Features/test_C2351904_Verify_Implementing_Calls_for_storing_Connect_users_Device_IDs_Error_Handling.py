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
class Test_C2351904_Verify_Implementing_Calls_for_storing_Connect_users_Device_IDs_Error_Handling(Common):
    """
    TR_ID: C2351904
    NAME: Verify Implementing Calls for storing Connect users Device IDs (Error Handling)
    DESCRIPTION: This test case verifies the error handling of implementing calls for storing, getting, and deleting Connect users Device IDs
    PRECONDITIONS: Links for dev0 environment:
    PRECONDITIONS: https://optin-dev0.coralsports.dev.cloud.ladbrokescoral.com/api/connect/save?deviceId={device Id value}
    PRECONDITIONS: https://optin-dev0.coralsports.dev.cloud.ladbrokescoral.com/api/connect/get?deviceId={device Id value}
    PRECONDITIONS: https://optin-dev0.coralsports.dev.cloud.ladbrokescoral.com/api/connect/remove?deviceId={device Id value}
    """
    keep_browser_open = True

    def test_001_try_to_save_device_idgo_to_httpsoptin_dev0coralsportsdevcloudladbrokescoralcomapiconnectsavedeviceid(self):
        """
        DESCRIPTION: Try to save device id:
        DESCRIPTION: go to https://optin-dev0.coralsports.dev.cloud.ladbrokescoral.com/api/connect/save?deviceId=
        EXPECTED: The system returns { "status": "ERROR", "message": "Please provide deviceId parameter", "id": ""}
        """
        pass

    def test_002_try_to_get_device_idgo_to_httpsoptin_dev0coralsportsdevcloudladbrokescoralcomapiconnectgetdeviceid(self):
        """
        DESCRIPTION: Try to get device id:
        DESCRIPTION: go to https://optin-dev0.coralsports.dev.cloud.ladbrokescoral.com/api/connect/get?deviceId=
        EXPECTED: The system returns { "status": "ERROR", "message": "Please provide deviceId parameter", "id": ""}
        """
        pass

    def test_003_try_to_delete_device_idhttpsoptin_dev0coralsportsdevcloudladbrokescoralcomapiconnectremovedeviceid(self):
        """
        DESCRIPTION: Try to delete device id:
        DESCRIPTION: https://optin-dev0.coralsports.dev.cloud.ladbrokescoral.com/api/connect/remove?deviceId=
        EXPECTED: The system returns { "status": "ERROR", "message": "Please provide deviceId parameter", "id": ""}
        """
        pass

    def test_004_get_non_existent_device_idgo_to_httpsoptin_dev0coralsportsdevcloudladbrokescoralcomapiconnectgetdeviceiddevice_id_value(self):
        """
        DESCRIPTION: Get non existent device id:
        DESCRIPTION: go to https://optin-dev0.coralsports.dev.cloud.ladbrokescoral.com/api/connect/get?deviceId={device Id value}
        EXPECTED: The system returns { "status": "ERROR", message: ''Can't find device by id: {device Id value}", ''id'': ''{device Id value}''}
        """
        pass

    def test_005_delete_non_existent_device_idhttpsoptin_dev0coralsportsdevcloudladbrokescoralcomapiconnectremovedeviceiddevice_id_value(self):
        """
        DESCRIPTION: Delete non existent device id:
        DESCRIPTION: https://optin-dev0.coralsports.dev.cloud.ladbrokescoral.com/api/connect/remove?deviceId={device Id value}
        EXPECTED: The system returns { "status": "ERROR", "message": "Can't delete non existent device by id : {device id}", "id": "{device id}"}
        """
        pass
