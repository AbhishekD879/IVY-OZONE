import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C57732116_Verify_retrieving_of_Win_Loose_status_for_events_from_SiteServer(Common):
    """
    TR_ID: C57732116
    NAME: Verify retrieving of Win/Loose status for events from SiteServer
    DESCRIPTION: This test case verifies retrieving of Win/Loose status for events from SiteServer
    PRECONDITIONS: Please look for some insights on a pages as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/Symphony+Infrastructure+creds
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+run+unpublished+Qubit+variation+on+Ladbrokes
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+generate+Live+Score+updates+on+Tennis+and+Football+sports
    PRECONDITIONS: 1. User is logged In
    """
    keep_browser_open = True

    def test_001_open_current_tab_and_make_a_prediction(self):
        """
        DESCRIPTION: Open 'Current Tab' and make a prediction
        EXPECTED: Precondition is successfully saved
        """
        pass

    def test_002_wait_until_event_ends_with_winloose_result_for_user_or_configure_it_manually_httpsconfluenceegalacoralcomdisplayspihowplustoplusgenerateplusliveplusscoreplusupdatesplusonplustennisplusandplusfootballplussports(self):
        """
        DESCRIPTION: Wait until event ends with Win/Loose result for user or configure it manually (https://confluence.egalacoral.com/display/SPI/How+to+generate+Live+Score+updates+on+Tennis+and+Football+sports)
        EXPECTED: - Every XX seconds since event start time microservice get Active Game from CMS (default value is 20 seconds)
        EXPECTED: - Every YY seconds since event start time microservice check results of event (default value is 20 seconds)
        EXPECTED: - Results scores displayed accordingly to each event
        EXPECTED: - Win/Loose indicator displayed accordingly to each event
        """
        pass
