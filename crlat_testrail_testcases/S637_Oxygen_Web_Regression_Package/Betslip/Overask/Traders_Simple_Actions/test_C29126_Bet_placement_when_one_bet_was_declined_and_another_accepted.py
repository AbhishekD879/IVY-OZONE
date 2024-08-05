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
class Test_C29126_Bet_placement_when_one_bet_was_declined_and_another_accepted(Common):
    """
    TR_ID: C29126
    NAME: Bet placement when one bet was declined and another accepted
    DESCRIPTION: This test case verifies Bet Slip functionality and UI when one bet was accepted and another rejected
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. User is logged in to the app
    PRECONDITIONS: 3. Overask functionality is enabled for the user
    PRECONDITIONS: 4. Go to CMS >'System-configuration' section > Config' tab > find 'Overask' config
    PRECONDITIONS: 5. Initial Data' checkbox is present within 'Overask' config and unchecked by default
    PRECONDITIONS: 6. The Initial response of the config contains 'The initialDataConfig: false'
    PRECONDITIONS: 7. The Initial Data response on homepage is absent
    PRECONDITIONS: CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: Overask:
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?pageId=41190983
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?pageId=41190955
    PRECONDITIONS: ![](index.php?/attachments/get/109045765)
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is loaded
        """
        pass

    def test_002_add_two_selections_and_go_to_betslip_singles_section(self):
        """
        DESCRIPTION: Add two selections and go to Betslip, 'Singles' section
        EXPECTED: 
        """
        pass

    def test_003_enter_value_in_stake_field_that_exceedsmax_allowed_bet_limit_for_two_selections_and_click__tap__place_bet_button(self):
        """
        DESCRIPTION: Enter value in 'Stake' field that exceeds max allowed bet limit for two selections and click / tap  'Place bet' button
        EXPECTED: The bet is sent to Openbet system for review
        """
        pass

    def test_004_verify_betslip(self):
        """
        DESCRIPTION: Verify Betslip
        EXPECTED: *   CMS configurable title, topMessage and bottomMessage for OverAsk are displayed on an overlay on white background anchored to the footer.
        EXPECTED: *   Green (Coral) and black (Ladbrokes) loading spinner is centred and shown between title and text
        EXPECTED: * Background is disabled and not clickable
        """
        pass

    def test_005____trigger_rejecting_the_first_bet_by_a_trader_in_openbet_system___trigger_accepting_the_second_bet_by_a_trader_in_openbet_system(self):
        """
        DESCRIPTION: *   Trigger rejecting the first bet by a trader in OpenBet system
        DESCRIPTION: *   Trigger accepting the second bet by a trader in OpenBet system
        EXPECTED: *   First bet is rejected in OpenBet, Second bet is accepted.
        EXPECTED: *   Confirmation and the reason of rejecting are sent and received in Oxygen app
        """
        pass

    def test_006_verify_betslip(self):
        """
        DESCRIPTION: Verify Betslip
        EXPECTED: * Accepted Bet has a message saying '(X) Bet Placed Successfully' within a bet receipt
        EXPECTED: * 'This bet has not been accepted by traders!' message is displayed for declined bet
        EXPECTED: * 'Go Betting' button is present and enabled ('Reuse Selections' button is absent)
        EXPECTED: ![](index.php?/attachments/get/33995) ![](index.php?/attachments/get/33994)
        """
        pass

    def test_007_click__tap_continuego_betting_from_ox_99_button(self):
        """
        DESCRIPTION: Click / tap 'Continue'/'Go Betting' (From OX 99) button
        EXPECTED: * Betslip is closed
        EXPECTED: * User is redirected to the Home page (?)
        """
        pass

    def test_008_add_a_few_selections_and_go_betslip_multiples_section(self):
        """
        DESCRIPTION: Add a few selections and go Betslip, 'Multiples' section
        EXPECTED: 
        """
        pass

    def test_009_repeat_steps__3_7_for_multiple_bet(self):
        """
        DESCRIPTION: Repeat steps № 3-7 for Multiple bet
        EXPECTED: 
        """
        pass

    def test_010_add_a_few_selections_from_the_same_race_event_and_go_betslip_forecaststricasts_section(self):
        """
        DESCRIPTION: Add a few selections from the same <Race> event and go Betslip, 'Forecasts/Tricasts' section
        EXPECTED: 
        """
        pass

    def test_011_repeat_steps__3_6_for_forecaststricastsbet(self):
        """
        DESCRIPTION: Repeat steps № 3-6 for Forecasts/Tricasts bet
        EXPECTED: 
        """
        pass
