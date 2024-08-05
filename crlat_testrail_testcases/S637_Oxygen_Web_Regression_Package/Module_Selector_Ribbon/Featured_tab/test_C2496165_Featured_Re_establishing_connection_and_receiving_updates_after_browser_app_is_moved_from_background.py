import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.homepage_featured
@vtest
class Test_C2496165_Featured_Re_establishing_connection_and_receiving_updates_after_browser_app_is_moved_from_background(Common):
    """
    TR_ID: C2496165
    NAME: Featured: Re-establishing connection and receiving updates after browser/app is moved from background
    DESCRIPTION: This test case verifies re-establishing connection to Featured microservice and receiving updates when user brings a browser/app from the background in order to receive the latest Featured Events data
    PRECONDITIONS: * There are featured modules with data configured in CMS
    PRECONDITIONS: * User is on the Home page
    PRECONDITIONS: * Browser console is opened
    PRECONDITIONS: Note:
    PRECONDITIONS: * For now Featured microservice makes ~20 attempts to reconnect when internet connection is lost or during sleep mode. For proper testing web-socket connection should be lost completely, so move app/browser to background for ~10 minutes (attempts to reconnect can be checked in web console)
    """
    keep_browser_open = True

    def test_001_move_app_to_background_for_as_much_time_so_websocket_connection_to_featured_microservice_is_completely_lost_see_preconditions(self):
        """
        DESCRIPTION: Move app to background for as much time, so websocket connection to Featured microservice is completely lost (see Preconditions)
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

    def test_004_move_app_to_foregroundverify_console(self):
        """
        DESCRIPTION: Move app to foreground
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
