import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.virtual_sports
@vtest
class Test_C869660_Select_Price_Odds_buttons_for_Started_Event(Common):
    """
    TR_ID: C869660
    NAME: Select Price/Odds buttons for Started Event
    DESCRIPTION: This test case verifies selecting Price/Odds buttons for already started event
    DESCRIPTION: NOTE, **User Story: **BMA-3156 [Customer can add VS selections to the BMA bet slip]
    PRECONDITIONS: Make sure that event is started but not yet finished
    """
    keep_browser_open = True

    def test_001_go_to_virtual_sports(self):
        """
        DESCRIPTION: Go to 'Virtual Sports'
        EXPECTED: Virtual Sports successfully opened
        EXPECTED: Next or current event is shown
        """
        pass

    def test_002_go_to_virtual_football_sport_page(self):
        """
        DESCRIPTION: Go to 'Virtual Football' sport page
        EXPECTED: 'Virtual Football' sport page is opened
        """
        pass

    def test_003_wait_untill_event_is_started_isstarted__true_in_siteserver_response(self):
        """
        DESCRIPTION: Wait untill event is started (isStarted = true in SiteServer response)
        EXPECTED: "Live" label appears above the sport icon in the carousel instead of event countdown timer
        """
        pass

    def test_004_check_market_sections(self):
        """
        DESCRIPTION: Check market sections
        EXPECTED: 'Price/Odds' buttons become greyed out
        """
        pass

    def test_005_try_to_add_selection_to_the_betslip_for_this_event(self):
        """
        DESCRIPTION: Try to add selection to the Betslip for this event
        EXPECTED: When event starts it is impossible to select 'Price/Odds' buttons, all buttons are disabled
        """
        pass

    def test_006_repeat_this_test_case_for_the_following_virtual_sports_football_speedway_tennis(self):
        """
        DESCRIPTION: Repeat this test case for the following virtual sports:
        DESCRIPTION: * Football,
        DESCRIPTION: * Speedway,
        DESCRIPTION: * Tennis
        EXPECTED: 
        """
        pass
