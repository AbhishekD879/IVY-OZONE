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
class Test_C869678_Select_Price_Odds_buttons_for_Started_Event(Common):
    """
    TR_ID: C869678
    NAME: Select Price/Odds buttons for Started Event
    DESCRIPTION: This test case verifies selecting Price/Odds buttons for already started event
    DESCRIPTION: NOTE, **User Story:** BMA-3156 [Customer can add VS selections to the BMA bet slip]
    PRECONDITIONS: Make sure that event is started but not yet finished
    PRECONDITIONS: List of relevant class IDs:
    PRECONDITIONS: Virtual Motorsports (Class ID 288)
    PRECONDITIONS: Virtual Cycling (Class ID 290)
    PRECONDITIONS: Virtual Horse Racing (Class ID 285)
    PRECONDITIONS: Virtual Greyhound Racing (Class ID 286)
    PRECONDITIONS: Virtual Grand National (Class ID 26604)
    PRECONDITIONS: 1. Open Coral/Ladbrokes test environment
    PRECONDITIONS: 2. Go to 'Virtual Sports'
    """
    keep_browser_open = True

    def test_001_wait_untill_event_is_started_isstarted__true_in_siteserver_response(self):
        """
        DESCRIPTION: Wait untill event is started (isStarted = true in SiteServer response)
        EXPECTED: Label "Live Now" appears instead of event countdown timer
        """
        pass

    def test_002_check_market_sections(self):
        """
        DESCRIPTION: Check market sections
        EXPECTED: 'Price/Odds' buttons become greyed out
        """
        pass

    def test_003_try_to_add_selection_to_the_betslip_for_this_event(self):
        """
        DESCRIPTION: Try to add selection to the Betslip for this event
        EXPECTED: When event starts it is impossible to select 'Price/Odds' buttons, all buttons are disabled
        """
        pass

    def test_004_repeat_this_test_case_for_all_virtual_raceslist_of_relevant_class_ids_virtual_motorsports_class_id_288_virtual_cycling_class_id_290_virtual_horse_racing_class_id_285_virtual_greyhound_racing_class_id_286_virtual_grand_national_class_id_26604(self):
        """
        DESCRIPTION: Repeat this test case for all Virtual Races:
        DESCRIPTION: List of relevant class IDs:
        DESCRIPTION: * Virtual Motorsports (Class ID 288)
        DESCRIPTION: * Virtual Cycling (Class ID 290)
        DESCRIPTION: * Virtual Horse Racing (Class ID 285)
        DESCRIPTION: * Virtual Greyhound Racing (Class ID 286)
        DESCRIPTION: * Virtual Grand National (Class ID 26604)
        EXPECTED: 
        """
        pass
