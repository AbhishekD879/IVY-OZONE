import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.betslip
@vtest
class Test_C29124_Reject_a_Bet(Common):
    """
    TR_ID: C29124
    NAME: Reject a Bet
    DESCRIPTION: This test case verifies rejecting of a bet by a trader triggered by overask functionality
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

    def test_001_add_selection_and_go_betslip_singles_section(self):
        """
        DESCRIPTION: Add selection and go Betslip, 'Singles' section
        EXPECTED: 
        """
        pass

    def test_002_enter_value_in_stake_field_that_exceedsmax_allowed_bet_limit_for_particular_selection_and_click__tap_bet_now_button_place_bet_from_ox_99_button(self):
        """
        DESCRIPTION: Enter value in 'Stake' field that exceeds max allowed bet limit for particular selection and click / tap 'Bet Now' button/ 'Place bet' (From OX 99) button
        EXPECTED: The bet is sent to Openbet system for review
        """
        pass

    def test_003_verify_betslip(self):
        """
        DESCRIPTION: Verify Betslip
        EXPECTED: *   CMS configurable title, topMessage and bottomMessage for OverAsk are displayed on an overlay on white background anchored to the footer.
        EXPECTED: *   Green (Coral) and black (Ladbrokes) loading spinner is centred and shown between title and text
        EXPECTED: * Background is disabled and not clickable
        """
        pass

    def test_004_trigger_rejecting_the_bet_by_a_trader_in_openbet_system(self):
        """
        DESCRIPTION: Trigger rejecting the bet by a trader in OpenBet system
        EXPECTED: *   The bet is rejected in OpenBet
        EXPECTED: *   Confirmation and the reason of rejecting are sent and received in the app
        """
        pass

    def test_005_verify_betslip(self):
        """
        DESCRIPTION: Verify Betslip
        EXPECTED: *   Bet is not placed and a 'This bet has not been accepted by traders!' message is shown on **Bet receipt**
        EXPECTED: * 'Stake' field disappears
        EXPECTED: * 'Go betting' button is present ('Reuse Selections' button is absent)
        EXPECTED: * Balance is not reduced
        EXPECTED: ![](index.php?/attachments/get/33805) ![](index.php?/attachments/get/33804)
        """
        pass

    def test_006_clicktap_go_betting_button(self):
        """
        DESCRIPTION: Click/Tap 'Go betting' button
        EXPECTED: *   Betslip is cleared automatically
        EXPECTED: *   'You have no selections in the slip' message is shown (tablet, desktop)
        EXPECTED: *   Betslip is closed automatically (mobile)
        """
        pass

    def test_007_add_a_few_selections_and_go_betslip_multiples_section(self):
        """
        DESCRIPTION: Add a few selections and go Betslip, 'Multiples' section
        EXPECTED: 
        """
        pass

    def test_008_repeat_steps__3_7_for_multiple_bet(self):
        """
        DESCRIPTION: Repeat steps № 3-7 for Multiple bet
        EXPECTED: 
        """
        pass

    def test_009_add_a_few_selections_from_the_same_race_event_and_go_betslip_forecaststricasts_section(self):
        """
        DESCRIPTION: Add a few selections from the same <Race> event and go Betslip, 'Forecasts/Tricasts' section
        EXPECTED: 
        """
        pass

    def test_010_repeat_steps__3_6_for_forecaststricastsbet(self):
        """
        DESCRIPTION: Repeat steps № 3-6 for Forecasts/Tricasts bet
        EXPECTED: 
        """
        pass
