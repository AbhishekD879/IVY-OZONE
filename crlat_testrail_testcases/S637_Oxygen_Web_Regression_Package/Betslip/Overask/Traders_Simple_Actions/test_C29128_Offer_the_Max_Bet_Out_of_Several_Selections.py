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
class Test_C29128_Offer_the_Max_Bet_Out_of_Several_Selections(Common):
    """
    TR_ID: C29128
    NAME: Offer the Max Bet Out of Several Selections
    DESCRIPTION: This test case verifies offering the maximum value for one bet out of several selections by a trader triggered by overask functionality
    DESCRIPTION: *   BMA-6574 Overask - Trader's Simple actions
    DESCRIPTION: *   BMA-20390 New Betslip - Overask design improvements
    PRECONDITIONS: User is logged in
    PRECONDITIONS: TO UPDATE 'Accept & Bet' button is missing
    PRECONDITIONS: https://app.zeplin.io/project/5c892a4a1f719638a3fb8b0a/screen/5c892a87988ef41982599fbf
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

    def test_002_add_selections_and_go_betslip_singles_section(self):
        """
        DESCRIPTION: Add selections and go Betslip, 'Singles' section
        EXPECTED: 
        """
        pass

    def test_003_enter_value_in_stake_field_that_exceedsmax_allowed_bet_limit_for_one_of_added_selections_and_click__tap_bet_now_button(self):
        """
        DESCRIPTION: Enter value in 'Stake' field that exceeds max allowed bet limit for one of added selections and click / tap 'Bet Now' button
        EXPECTED: The bet is sent to Openbet system for review
        """
        pass

    def test_004_verify_betslip(self):
        """
        DESCRIPTION: Verify Betslip
        EXPECTED: * 'Please wait, your bet is being reviewed by one of our Traders. This normally takes less than a minute.' message is displayed on yellow background anchored to the footer of the Betslip
        EXPECTED: * Loading spinner is displayed on the green button, replacing 'Bet Now' label
        EXPECTED: * 'Stake', 'Est. Returns' fields, 'Clear Betslip' and 'Bet Now' buttons are disabled and greyed out
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
        EXPECTED: *   Selection with the maximum bet offer is expanded
        EXPECTED: *   The maximum bet offer for selected on step #3 bet and enabled checked checkbox are shown to user
        EXPECTED: *   Message 'Note: You're accepting this Trade Offer' appears on the grey background below the checked selection
        EXPECTED: *   The rest of selections are shown unchanged
        EXPECTED: *   'Accept & Bet ([number of accepted bets])' and 'Cancel' buttons are present
        EXPECTED: *   'Accept & Bet ([number of accepted bets])' and 'Cancel' buttons are enabled
        """
        pass

    def test_007_click__tap_accept__bet_button(self):
        """
        DESCRIPTION: Click / tap 'Accept & Bet' button
        EXPECTED: *   Bets are placed and balance is reduced accordingly
        EXPECTED: *   Bets are listed in 'Bet History' and 'My Account' pages
        """
        pass

    def test_008_repeat_steps__2_7(self):
        """
        DESCRIPTION: Repeat steps # 2-7
        EXPECTED: 
        """
        pass

    def test_009_click__tap_cancel_button(self):
        """
        DESCRIPTION: Click / tap 'Cancel' button
        EXPECTED: *   Bets are NOT placed
        EXPECTED: *   Selections are still present in Betslip
        EXPECTED: *   'Stake', 'Est.Returns', 'Total Stake' and 'Total Est. Returns' fields are empty
        """
        pass

    def test_010_add_a_few_selections_and_go_betslip_multiples_section(self):
        """
        DESCRIPTION: Add a few selections and go Betslip, 'Multiples' section
        EXPECTED: 
        """
        pass

    def test_011_repeat_steps__3_10_for_multiple_bet(self):
        """
        DESCRIPTION: Repeat steps № 3-10 for Multiple bet
        EXPECTED: 
        """
        pass

    def test_012_add_a_few_selections_from_the_same_race_event_and_go_betslip_forecaststricasts_section(self):
        """
        DESCRIPTION: Add a few selections from the same <Race> event and go Betslip, 'Forecasts/Tricasts' section
        EXPECTED: 
        """
        pass

    def test_013_repeat_steps__3_10_for_forecaststricastsbet(self):
        """
        DESCRIPTION: Repeat steps № 3-10 for Forecasts/Tricasts bet
        EXPECTED: 
        """
        pass
