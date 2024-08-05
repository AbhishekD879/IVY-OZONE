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
class Test_C44870221_Betslip_Live_push_Suspension(Common):
    """
    TR_ID: C44870221
    NAME: Betslip Live push /Suspension
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_launch_the_app_enter_with_valid_credentials(self):
        """
        DESCRIPTION: Launch the app enter with valid credentials
        EXPECTED: Application launched successfully and User should be logged in successfully
        """
        pass

    def test_002_go_to_in_play_steaming_from_home_page(self):
        """
        DESCRIPTION: Go to 'In-play &steaming' from home page
        EXPECTED: User should be on in-play page
        """
        pass

    def test_003_add_some_selections_from_any_in_play_events_from_any_market_for_different_sports_and_verify_the_bet_slip_with_live_push_when_price_changes(self):
        """
        DESCRIPTION: Add some selections from any in-play events from any market for different sports And Verify the bet slip with Live Push when price changes
        EXPECTED: User must be presented with all the selection from different markets to the Bet slip and User must presented with the top message in the Bet slip
        EXPECTED: Price change notification
        EXPECTED: "Some of your prices have changed"
        """
        pass

    def test_004_verify_the_bet_slip_with_live_push_when_price_changes_for_the_added_selections(self):
        """
        DESCRIPTION: Verify the bet slip with Live Push when price changes for the added selections
        EXPECTED: User must be presented with the message just above the selection in the Bet slip like
        EXPECTED: 'Price changed from x/x to x/x' for all the changed prices
        """
        pass

    def test_005_verify_the_place_bet_button_text_update(self):
        """
        DESCRIPTION: Verify the 'Place Bet' button text update
        EXPECTED: User must be presented with the replaced of 'Place Bet' button with 'Accept & Continue' button
        """
        pass

    def test_006_verify_when_user_clicks_on_any_sports_or_races_virtual(self):
        """
        DESCRIPTION: Verify when user clicks on any sports or races (Virtual)
        EXPECTED: User must be on particular page page
        """
        pass

    def test_007_add_selections_to_bet_slip(self):
        """
        DESCRIPTION: Add selections to bet slip
        EXPECTED: Selection should have been added in to bet slip
        """
        pass

    def test_008_verify_when_the_event_starts__suspension_displayed_in_bet_slip(self):
        """
        DESCRIPTION: Verify when the event starts , suspension displayed in bet slip
        EXPECTED: Suspension must be displayed in bet slip and user must not be able to place bet.
        """
        pass
