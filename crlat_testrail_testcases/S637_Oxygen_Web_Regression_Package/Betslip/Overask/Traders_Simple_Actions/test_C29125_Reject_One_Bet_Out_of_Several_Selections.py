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
class Test_C29125_Reject_One_Bet_Out_of_Several_Selections(Common):
    """
    TR_ID: C29125
    NAME: Reject One Bet Out of Several Selections
    DESCRIPTION: This test case verifies rejecting of one bet out of several selections by a trader triggered by overask functionality
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

    def test_002_add_a_few_selections_and_go_betslip(self):
        """
        DESCRIPTION: Add a few selections and go Betslip
        EXPECTED: The selections are added to betslip
        """
        pass

    def test_003_enter_value_in_stake_fields_that_does_not_exceed_max_allowed_bet_limitfor_one_of_added_selections(self):
        """
        DESCRIPTION: Enter value in 'Stake' fields that does not exceed max allowed bet limit for one of added selections
        EXPECTED: 'Stake' field is populated with value
        """
        pass

    def test_004_leave_at_least_one_stake_field_empty(self):
        """
        DESCRIPTION: Leave at least one 'Stake' field empty
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
        EXPECTED: *   CMS configurable title, topMessage and bottomMessage for OverAsk are displayed on an overlay on white background anchored to the footer.
        EXPECTED: *   Green (Coral) and black (Ladbrokes) loading spinner is centred and shown between title and text
        EXPECTED: * Background is disabled and not clickable
        """
        pass

    def test_007_trigger_rejecting_the_bet_by_a_trader_in_openbet_system(self):
        """
        DESCRIPTION: Trigger rejecting the bet by a trader in OpenBet system
        EXPECTED: *   The bet is rejected in OpenBet
        EXPECTED: *   Confirmation is sent and received in Oxygen app
        """
        pass

    def test_008_verify_betslip(self):
        """
        DESCRIPTION: Verify Betslip
        EXPECTED: * Auto-accepted bet is placed and Bet Receipt is displayed
        EXPECTED: * Rejected bet is not placed and a 'This bet has not been accepted by traders!' message is shown
        EXPECTED: * Bet with empty 'Stake' field is ignored and not placed
        EXPECTED: * 'Go betting' button is present ('Reuse Selections' button is absent)
        EXPECTED: * Balance is reduced accordingly
        EXPECTED: * Auto-accepted bet is listed in 'Bet History' and 'My Account' pages
        EXPECTED: ![](index.php?/attachments/get/33996) ![](index.php?/attachments/get/33997)
        """
        pass

    def test_009_click__tap_continue_go_betting_from_ox_99_button(self):
        """
        DESCRIPTION: Click / tap 'Continue'/ 'Go betting' (From OX 99) button
        EXPECTED: * Betslip is cleared automatically
        EXPECTED: * 'You have no selections in the slip' message is shown (tablet, desktop)
        EXPECTED: * Betslip is closed automatically (mobile)
        """
        pass

    def test_010_add_a_few_selections_and_go_betslip_multiples_section(self):
        """
        DESCRIPTION: Add a few selections and go Betslip, 'Multiples' section
        EXPECTED: 
        """
        pass

    def test_011_repeat_steps_2_9_but_on_step_5_enter_max_value_in_stake_field_for_multiple_bet(self):
        """
        DESCRIPTION: Repeat steps #2-9 but on step #5 enter max value in 'Stake' field for Multiple bet
        EXPECTED: 
        """
        pass

    def test_012_add_a_few_selections_from_the_same_race_event_and_go_betslip_forecaststricasts_section(self):
        """
        DESCRIPTION: Add a few selections from the same <Race> event and go Betslip, 'Forecasts/Tricasts' section
        EXPECTED: 
        """
        pass

    def test_013_repeat_steps_2_9_but_on_step_5_enter_max_value_in_stake_field_for_forecaststricasts_bet(self):
        """
        DESCRIPTION: Repeat steps #2-9 but on step #5 enter max value in 'Stake' field for Forecasts/Tricasts bet
        EXPECTED: 
        """
        pass
