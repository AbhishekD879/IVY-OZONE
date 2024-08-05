import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C28499_Verify_Price_Odds_buttons_view_before_and_after_adding_to_betslip(Common):
    """
    TR_ID: C28499
    NAME: Verify Price/Odds buttons view before and after adding to betslip
    DESCRIPTION: This test case verifies Price/Odds buttons view before selecting them and after
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Home page is opened
        """
        pass

    def test_002_tap_live_icon_from_the_sports_ribbon(self):
        """
        DESCRIPTION: Tap '**LIVE**' icon from the sports ribbon
        EXPECTED: 'In-Play' Landing page is opened
        """
        pass

    def test_003_tap_sport_icon_from_live_sports_ribbon(self):
        """
        DESCRIPTION: Tap <Sport> icon from live sports ribbon
        EXPECTED: <Sport> In-Play page is opened
        """
        pass

    def test_004_choose_live_now_sorting_type(self):
        """
        DESCRIPTION: Choose '**Live Now**' sorting type
        EXPECTED: Live Now events are displayed
        """
        pass

    def test_005_verify_the_priceodds_buttons_view_of_the_events_displayed(self):
        """
        DESCRIPTION: Verify the 'Price/Odds' buttons view of the events displayed
        EXPECTED: *    'Price/Odds' buttons display price received from backend on light grey background.
        EXPECTED: *    'Price/Odds' buttons display selection type (e.gHome, Draw, Away)
        """
        pass

    def test_006_click_on_priceodds_button_and_check_its_displaying(self):
        """
        DESCRIPTION: Click on price/odds button and check it's displaying
        EXPECTED: Button becomes green
        """
        pass

    def test_007_verify_that_selection_is_added_to_bet_slip(self):
        """
        DESCRIPTION: Verify that selection is added to Bet Slip
        EXPECTED: *   Selection is shown in Betslip widget/Slide Out Betslip
        EXPECTED: *   Selection is present in Bet Slip and counter is increased on header
        """
        pass

    def test_008_remove_selection_from_bet_slip(self):
        """
        DESCRIPTION: Remove selection from Bet Slip
        EXPECTED: *   Selection is removed
        EXPECTED: *   Price/odds button becomes light grey
        """
        pass

    def test_009_check_price_type_changing_from_decimal_to_fractional_and_vice_versa(self):
        """
        DESCRIPTION: Check Price type changing from Decimal to Fractional and vice versa
        EXPECTED: Prices format is changed on buttons depending what format was selectedDese
        """
        pass

    def test_010_select_upcoming_sorting_type_and_repeat_steps_5_9(self):
        """
        DESCRIPTION: Select 'Upcoming' sorting type and repeat steps 5-9
        EXPECTED: 
        """
        pass

    def test_011_repeat_steps_5_9_on_in_play_widget(self):
        """
        DESCRIPTION: Repeat steps #5-9 on 'In play' widget
        EXPECTED: 
        """
        pass

    def test_012_navigate_to_event_details_page_and_repeat_steps5_9(self):
        """
        DESCRIPTION: Navigate to Event Details Page and repeat steps#5-9
        EXPECTED: 
        """
        pass

    def test_013_select_to_betslip_at_least_5_selections_and_check_the_price_odds_button_displaying(self):
        """
        DESCRIPTION: Select to betslip at least 5 selections and check the price odds button displaying
        EXPECTED: *   Selected Buttons becomes green
        EXPECTED: *   Selections are added to Betslip
        """
        pass
