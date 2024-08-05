import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@vtest
class Test_C9726253_Event_Hub_Re_establishing_connection_and_receiving_updates_after_lost_internet_connection(Common):
    """
    TR_ID: C9726253
    NAME: Event Hub: Re-establishing connection and receiving updates after lost internet connection
    DESCRIPTION: This test case verifies re-establishing connection to Featured microservice and receiving updates when connection is lost in order to receive the latest Featured Events data
    PRECONDITIONS: * There is At least 1 Event Hub with data configured in CMS
    PRECONDITIONS: * User is on the Home page > Event Hub tab
    PRECONDITIONS: * Browser console is opened
    PRECONDITIONS: Note:
    PRECONDITIONS: * For now Featured microservice makes ~20 attempts to reconnect when internet connection is lost. For proper testing web-socket connection should be lost completely, so device should lose internet connection (attempts to reconnect can be checked in web console)
    """
    keep_browser_open = True

    def test_001_make_device_lose_internet_connection_for_as_much_time_so_websocket_connection_to_featured_microservice_is_completely_lost_see_preconditions(self):
        """
        DESCRIPTION: Make device lose internet connection for as much time, so websocket connection to Featured microservice is completely lost (see Preconditions)
        EXPECTED: 
        """
        pass

    def test_002_trigger_module_websocket_updates_via_cms(self):
        """
        DESCRIPTION: Trigger module websocket updates via CMS
        EXPECTED: 
        """
        pass

    def test_003_trigger_liveserve_update_suspension_price_change_etc(self):
        """
        DESCRIPTION: Trigger LiveServe update (suspension, price change etc.)
        EXPECTED: 
        """
        pass

    def test_004_restore_internet_connectionverify_console(self):
        """
        DESCRIPTION: Restore internet connection
        DESCRIPTION: Verify console
        EXPECTED: * 'reload components' in console
        EXPECTED: * new active websocket connection appears
        """
        pass

    def test_005_verify_featured_tab(self):
        """
        DESCRIPTION: Verify Featured tab
        EXPECTED: All updates triggered during internet connection being lost are received in new WS connection and are displayed on FE.
        """
        pass
