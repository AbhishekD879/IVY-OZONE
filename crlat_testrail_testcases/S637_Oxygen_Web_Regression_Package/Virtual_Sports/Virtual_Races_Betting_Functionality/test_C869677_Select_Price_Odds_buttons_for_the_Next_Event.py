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
class Test_C869677_Select_Price_Odds_buttons_for_the_Next_Event(Common):
    """
    TR_ID: C869677
    NAME: Select Price/Odds buttons for the Next Event
    DESCRIPTION: This test case verifies selecting Price/Odds buttons for the next event which is not yet started
    DESCRIPTION: NOTE, **User Story:** BMA-3156 [Customer can add VS selections to the BMA bet slip]
    PRECONDITIONS: Make sure that event won't start in a few minutes
    PRECONDITIONS: List of relevant class IDs:
    PRECONDITIONS: Virtual Motorsports (Class ID 288)
    PRECONDITIONS: Virtual Cycling (Class ID 290)
    PRECONDITIONS: Virtual Horse Racing (Class ID 285)
    PRECONDITIONS: Virtual Greyhound Racing (Class ID 286)
    PRECONDITIONS: Virtual Grand National (Class ID 26604)
    """
    keep_browser_open = True

    def test_001_open_virtual_sports(self):
        """
        DESCRIPTION: Open 'Virtual Sports'
        EXPECTED: Virtual Sports successfully opened
        EXPECTED: Next event is displayed
        """
        pass

    def test_002_select_one_selection(self):
        """
        DESCRIPTION: Select one selection
        EXPECTED: Selected 'Price/Odds' button is highlighted in green
        EXPECTED: Betslip counter is increased
        EXPECTED: Betslip icon with bet counter is shown
        """
        pass

    def test_003_select_several_selections(self):
        """
        DESCRIPTION: Select several selections
        EXPECTED: Selected Price/Odds buttons are highlighted in green
        EXPECTED: Betslip counter is increased
        EXPECTED: Betslip icon with bet counter is shown
        """
        pass

    def test_004_navigate_between_events___go_to_the_verified_event(self):
        """
        DESCRIPTION: Navigate between events -> go to the verified event
        EXPECTED: Selected 'Price/Odds' buttons remain selected after navigation between events
        """
        pass

    def test_005_navigate_to_other_kind_of_sport_and_move_back_to_horse_racing_sport_page___check_selected_priceodds_buttons(self):
        """
        DESCRIPTION: Navigate to other kind of sport and move back to Horse Racing sport page -> check selected price/odds buttons
        EXPECTED: Selected 'Price/Odds' buttons remain selected after navigation between sport pages
        """
        pass

    def test_006_refresh_the_page(self):
        """
        DESCRIPTION: Refresh the page
        EXPECTED: Selected 'Price/Odds' buttons remain selected after refresh
        """
        pass

    def test_007_repeat_this_test_case_for_all_virtual_races_virtual_motorsports_class_id_288_virtual_cycling_class_id_290_virtual_horse_racing_class_id_285_virtual_greyhound_racing_class_id_286_virtual_grand_national_class_id_26604(self):
        """
        DESCRIPTION: Repeat this test case for all Virtual Races:
        DESCRIPTION: * Virtual Motorsports (Class ID 288)
        DESCRIPTION: * Virtual Cycling (Class ID 290)
        DESCRIPTION: * Virtual Horse Racing (Class ID 285)
        DESCRIPTION: * Virtual Greyhound Racing (Class ID 286)
        DESCRIPTION: * Virtual Grand National (Class ID 26604)
        EXPECTED: 
        """
        pass
