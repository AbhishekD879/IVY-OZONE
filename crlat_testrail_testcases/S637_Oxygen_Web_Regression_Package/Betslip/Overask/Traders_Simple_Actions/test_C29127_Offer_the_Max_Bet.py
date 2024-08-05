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
class Test_C29127_Offer_the_Max_Bet(Common):
    """
    TR_ID: C29127
    NAME: Offer the Max Bet
    DESCRIPTION: This test case verifies offering the maximum bet by a trader triggered by overask functionality
    DESCRIPTION: *   BMA-6574 Overask - Trader's Simple actions
    DESCRIPTION: *   BMA-20390 New Betslip - Overask design improvements
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

    def test_002_add_selection_and_go_betslip_singles_section(self):
        """
        DESCRIPTION: Add selection and go Betslip, 'Singles' section
        EXPECTED: 
        """
        pass

    def test_003_enter_value_in_stake_field_that_exceedsmax_allowed_bet_limit_for_particular_selection_and_click__tap_bet_now_button_place_bet_from_ox_99_button(self):
        """
        DESCRIPTION: Enter value in 'Stake' field that exceeds max allowed bet limit for particular selection and click / tap 'Bet Now' button/ 'Place bet' (From OX 99) button
        EXPECTED: The bet is sent to Openbet system for review
        """
        pass

    def test_004_verify_betslip(self):
        """
        DESCRIPTION: Verify Betslip
        EXPECTED: *   Overask is triggered for the User
        EXPECTED: *   The bet review notification is shown to the User
        """
        pass

    def test_005_trigger_offer_with_the_max_bet_by_a_trader_in_openbet_system(self):
        """
        DESCRIPTION: Trigger offer with the max bet by a trader in OpenBet system
        EXPECTED: Confirmation is sent and received in Oxygen app
        """
        pass

    def test_006_verify_betslip(self):
        """
        DESCRIPTION: Verify Betslip
        EXPECTED: * 'Sorry your bet has not gone through, we are offering you the following bet as an alternative' message and 'Offer expires: X:XX' counter are shown on the top
        EXPECTED: * 'i'icon is displayed on the left side of the message
        EXPECTED: * Selection is expanded
        EXPECTED: * The new stake is shown to the user on the Betslip (highlighted in yellow color)
        EXPECTED: * The Estimate returns are updated according to new Stake value
        EXPECTED: * 'Cancel' and 'Place a bet' buttons enabled
        EXPECTED: ![](index.php?/attachments/get/34018) ![](index.php?/attachments/get/34019)
        """
        pass

    def test_007_repeat_steps__2_6(self):
        """
        DESCRIPTION: Repeat steps # 2-6
        EXPECTED: 
        """
        pass

    def test_008_click__tap_cancel_button(self):
        """
        DESCRIPTION: Click / tap 'Cancel' button
        EXPECTED: ‘Cancel Offer?’ pop up with a message ‘Moving away from this screen will cancel your offer. Are you sure you want to go ahead?’ and ‘No, Return’ and ‘Cancel Offer’ buttons, pop-up appears on the grey background
        """
        pass

    def test_009_click__tap_cancel_offer_button(self):
        """
        DESCRIPTION: Click / tap 'Cancel Offer' button
        EXPECTED: *   Betslip closes
        EXPECTED: *   Selection is not present in Betslip
        EXPECTED: *   User stays on the previous page
        """
        pass

    def test_010_add_a_few_selections_and_go_betslip_multiples_section(self):
        """
        DESCRIPTION: Add a few selections and go Betslip, 'Multiples' section
        EXPECTED: 
        """
        pass

    def test_011_repeat_steps_3_10_but_on_step_3_enter_max_value_in_stake_field_for_multiple_bet(self):
        """
        DESCRIPTION: Repeat steps #3-10 but on step #3 enter max value in 'Stake' field for Multiple bet
        EXPECTED: 
        """
        pass

    def test_012_add_a_few_selections_from_the_same_race_event_and_go_betslip_forecaststricasts_section(self):
        """
        DESCRIPTION: Add a few selections from the same <Race> event and go Betslip, 'Forecasts/Tricasts' section
        EXPECTED: 
        """
        pass

    def test_013_repeat_steps__3_6_for_forecaststricastsbet(self):
        """
        DESCRIPTION: Repeat steps № 3-6 for Forecasts/Tricasts bet
        EXPECTED: 
        """
        pass
