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
class Test_C869659_Select_Price_Odds_buttons_for_the_Next_Event(Common):
    """
    TR_ID: C869659
    NAME: Select Price/Odds buttons for the Next Event
    DESCRIPTION: This test case verifies selecting Price/Odds buttons for the next event which is not yet started
    DESCRIPTION: NOTE, **User Story: **BMA-3156 [Customer can add VS selections to the BMA bet slip]
    PRECONDITIONS: Make sure that event won't start in a few minutes
    """
    keep_browser_open = True

    def test_001_go_to_virtual_sports(self):
        """
        DESCRIPTION: Go to 'Virtual Sports'
        EXPECTED: Virtual Sports is successfully opened.
        EXPECTED: Next or current event is shown.
        """
        pass

    def test_002_go_to_virtual_football_sport_page(self):
        """
        DESCRIPTION: Go to 'Virtual Football' sport page
        EXPECTED: 1.  User is redirected to 'Virtual Football' sport page;
        EXPECTED: 2.  Next event is displayed
        """
        pass

    def test_003_select_one_selection(self):
        """
        DESCRIPTION: Select one selection
        EXPECTED: Selected 'Price/Odds' button is highlighted in green
        EXPECTED: Betslip counter is increased
        """
        pass

    def test_004_select_several_selections(self):
        """
        DESCRIPTION: Select several selections
        EXPECTED: Selected Price/Odds buttons are highlighted in green
        EXPECTED: Betslip counter is increased by the number of added selections
        """
        pass

    def test_005_navigate_between_events___go_to_the_verified_event(self):
        """
        DESCRIPTION: Navigate between events -> go to the verified event
        EXPECTED: Selected 'Price/Odds' buttons remain highlighted in green after navigation between events
        """
        pass

    def test_006_navigate_to_other_kind_of_sport_and_move_back_to_football_sport_page___check_selected_priceodds_buttons(self):
        """
        DESCRIPTION: Navigate to other kind of sport and move back to Football sport page -> check selected price/odds buttons
        EXPECTED: Selected 'Price/Odds' buttons remain highlighted in green after navigation between sport pages
        """
        pass

    def test_007_refresh_the_page(self):
        """
        DESCRIPTION: Refresh the page
        EXPECTED: Selected 'Price/Odds' buttons remain selected after refresh
        """
        pass

    def test_008_repeat_this_test_case_for_the_following_virtual_sports_football_speedway_tennis(self):
        """
        DESCRIPTION: Repeat this test case for the following virtual sports:
        DESCRIPTION: * Football,
        DESCRIPTION: * Speedway,
        DESCRIPTION: * Tennis
        EXPECTED: 
        """
        pass
