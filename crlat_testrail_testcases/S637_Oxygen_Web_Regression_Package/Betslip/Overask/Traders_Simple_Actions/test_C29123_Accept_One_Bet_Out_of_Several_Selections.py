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
class Test_C29123_Accept_One_Bet_Out_of_Several_Selections(Common):
    """
    TR_ID: C29123
    NAME: Accept One Bet Out of Several Selections
    DESCRIPTION: This test case verifies accepting of one bet out of several selections by a trader triggered by overask functionality
    PRECONDITIONS: User is logged in
    PRECONDITIONS: ======
    PRECONDITIONS: [How to accept/decline/make an Offer with Overask functionality](https://confluence.egalacoral.com/pages/viewpage.action?pageId=41190955)
    PRECONDITIONS: [How to disable/enable Overask functionality for User or Event Type](https://confluence.egalacoral.com/pages/viewpage.action?pageId=41190983)
    PRECONDITIONS: * Go to CMS >'System-configuration' section > Config' tab > find 'Overask' config
    PRECONDITIONS: * Initial Data' checkbox is present within 'Overask' config and unchecked by default
    PRECONDITIONS: * The Initial response of the config contains 'The initialDataConfig: false'
    PRECONDITIONS: * The Initial Data response on homepage is absent
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: ![](index.php?/attachments/get/109045765)
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is loaded
        """
        pass

    def test_002_add_a_few_selections_and_go_betslip_singles_section(self):
        """
        DESCRIPTION: Add a few selections and go Betslip, 'Singles' section
        EXPECTED: 
        """
        pass

    def test_003_enter_value_in_stake_fields_that_does_not_exceed_max_allowed_bet_limitfor_one_of_added_selections(self):
        """
        DESCRIPTION: Enter value in 'Stake' fields that does not exceed max allowed bet limit for one of added selections
        EXPECTED: 'Stake' field is populated with value
        """
        pass

    def test_004_leave_at_list_one_stake_field_empty(self):
        """
        DESCRIPTION: Leave at list one 'Stake' field empty
        EXPECTED: 'Stake' field is empty
        """
        pass

    def test_005_enter_value_in_stake_field_that_exceedsmax_allowed_bet_limit_for_one_of_added_selections_and_click__tap_bet_now_button_place_bet_from_ox_99_button(self):
        """
        DESCRIPTION: Enter value in 'Stake' field that exceeds max allowed bet limit for one of added selections and click / tap 'Bet Now' button/ 'Place bet' (From OX 99) button
        EXPECTED: The bet is sent to Openbet system for review
        """
        pass

    def test_006_verify_betslip(self):
        """
        DESCRIPTION: Verify Betslip
        EXPECTED: *   'Please wait, your bet is being reviewed by one of our Traders. This normally takes less than a minute.' message is displayed on yellow background above 'Bet now' button
        EXPECTED: *   Loading spinner is displayed on the green button, replacing 'Bet Now' label
        EXPECTED: *   'Stake','Est. Returns' fields, 'Clear Betslip' and 'Bet Now' buttons are disabled and greyed out
        EXPECTED: *   The rest of selections remain at Betslip
        EXPECTED: **From OX 99**
        EXPECTED: *   CMS configurable title, topMessage and bottomMessage for OverAsk are displayed on an overlay on white background anchored to the footer.
        EXPECTED: *   Green (Coral) and black (Ladbrokes) loading spinner is centred and shown between title and text
        EXPECTED: * Background is disabled and not clickable
        """
        pass

    def test_007_trigger_accepting_the_bet_by_a_trader_in_openbet_system(self):
        """
        DESCRIPTION: Trigger accepting the bet by a trader in OpenBet system
        EXPECTED: *   The bet is accepted in OpenBet
        EXPECTED: *   Confirmation is sent and received in Oxygen app
        """
        pass

    def test_008_verify_betslip(self):
        """
        DESCRIPTION: Verify Betslip
        EXPECTED: *   Accepted in OB system bet is placed successfully with the original amount
        EXPECTED: *   Bet with entered 'Stake' field on step #3 is placed with the original amount
        EXPECTED: *   Bet with empty 'Stake' field is ignored and not placed
        EXPECTED: *   Balance is reduced accordingly
        EXPECTED: *   Placed bets are listed in 'Bet History' and 'My Account' pages
        EXPECTED: **From OX 99**
        EXPECTED: * 'Go Betting' button is present and enabled
        EXPECTED: *  Bet is placed successfully with the original amount
        EXPECTED: *  Bet Receipt is displayed for a user
        EXPECTED: *  Balance is reduced accordingly
        EXPECTED: *  Bet is listed in 'Bet History' and 'My Account' pages
        EXPECTED: ![](index.php?/attachments/get/34017) ![](index.php?/attachments/get/34016)
        """
        pass

    def test_009_add_a_few_selections_and_go_betslip_multiples_section(self):
        """
        DESCRIPTION: Add a few selections and go Betslip, 'Multiples' section
        EXPECTED: 
        """
        pass

    def test_010_repeat_steps__3_8_for_multiple_bet(self):
        """
        DESCRIPTION: Repeat steps № 3-8 for Multiple bet
        EXPECTED: 
        """
        pass

    def test_011_add_a_few_selections_from_the_same_race_event_and_go_betslip_forecaststricasts_section(self):
        """
        DESCRIPTION: Add a few selections from the same <Race> event and go Betslip, 'Forecasts/Tricasts' section
        EXPECTED: 
        """
        pass

    def test_012_repeat_steps__3_8_for_forecaststricastsbet(self):
        """
        DESCRIPTION: Repeat steps № 3-8 for Forecasts/Tricasts bet
        EXPECTED: 
        """
        pass
