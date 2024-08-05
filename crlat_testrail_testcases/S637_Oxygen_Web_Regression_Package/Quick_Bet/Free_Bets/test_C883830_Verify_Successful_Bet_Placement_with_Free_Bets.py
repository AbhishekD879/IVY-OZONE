import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.quick_bet
@vtest
class Test_C883830_Verify_Successful_Bet_Placement_with_Free_Bets(Common):
    """
    TR_ID: C883830
    NAME: Verify Successful Bet Placement with Free Bets
    DESCRIPTION: This test case verifies Successful Bet Placement with Free Bets within Quick Bet
    PRECONDITIONS: 1.  Quick Bet functionality should be enabled in CMS and user`s settings
    PRECONDITIONS: 2.  Quick Bet functionality is available for Mobile ONLY
    PRECONDITIONS: 3.  User is logged in and has positive balance
    PRECONDITIONS: 4. The user should have free bets added to next levels:
    PRECONDITIONS: * all
    PRECONDITIONS: * class
    PRECONDITIONS: * type
    PRECONDITIONS: * event
    PRECONDITIONS: * market
    PRECONDITIONS: * selection
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+Manually+Add+Freebet+Token+to+Event
    PRECONDITIONS: 5. [How to add Free bets to user`s account] [1]
    PRECONDITIONS: [1]: https://confluence.egalacoral.com/display/SPI/How+to+Manually+Add+Freebet+Token+to+Account
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_add_selection_to_quick_bet_to_which_free_bet_token_is_applied_to_on_selection_level(self):
        """
        DESCRIPTION: Add selection to Quick Bet to which Free bet token is applied to on selection level
        EXPECTED: * Quick Bet is displayed at the bottom of the page
        EXPECTED: * "Use Free Bet" link is displayed under event name
        EXPECTED: "Place Bet" CTA is inactive, "Add to Betslip" active
        EXPECTED: ![](index.php?/attachments/get/31385)
        """
        pass

    def test_003_tap_use_free_bet_link_and_select_free_bet_token_which_is_applied_to_the_added_selectionfrom_ox100_tap_use_free_bet_link_and_select_free_bet_token_which_is_applied_to_the_added_selection_and_click_on_add_button(self):
        """
        DESCRIPTION: Tap "Use Free Bet" link and Select Free bet token which is applied to the added selection
        DESCRIPTION: *[From OX100]* Tap "Use Free Bet" link and Select Free bet token which is applied to the added selection AND click on 'ADD' button.
        EXPECTED: * Free bet is selected
        EXPECTED: * 'Stake' field is NOT changed
        EXPECTED: * Stake is equal to Free bet value
        EXPECTED: * 'PLACE BET' button becomes enabled
        EXPECTED: ![](index.php?/attachments/get/31386)
        EXPECTED: *[From OX100]*
        EXPECTED: * Free bet is selected
        EXPECTED: * 'Stake' field is NOT changed
        EXPECTED: * '- Remove Free Bet' link is displayed under the event name in the 'Quick bet'
        EXPECTED: * Total stake is updated with the Freebet value
        EXPECTED: * Free bet icon is displayed near Freebet value in the total stake
        EXPECTED: * Potential returns/Est returns based on odds taken also updated
        EXPECTED: * Free bet icon below the stake box is displayed in the 'Quick bet'
        EXPECTED: Coral design:
        EXPECTED: ![](index.php?/attachments/get/36196)
        EXPECTED: 'Stake' field is filled with 0.00:
        EXPECTED: ![](index.php?/attachments/get/36200)
        EXPECTED: Ladbrokes design:
        EXPECTED: ![](index.php?/attachments/get/36197)
        """
        pass

    def test_004_tap_place_bet_button(self):
        """
        DESCRIPTION: Tap 'PLACE BET' button
        EXPECTED: * Bet is placed successfully
        EXPECTED: * User balance is NOT changed
        EXPECTED: * Bet Receipt is shown
        EXPECTED: * Free bet icon is displayed near Freebet value for the stake in Bet Receipt:
        EXPECTED: Coral design:
        EXPECTED: ![](index.php?/attachments/get/36081)
        EXPECTED: Ladbrokes design:
        EXPECTED: ![](index.php?/attachments/get/36082)
        """
        pass

    def test_005_click_on_x_button(self):
        """
        DESCRIPTION: Click on 'X' button
        EXPECTED: Quick Bet is closed
        """
        pass

    def test_006_add_selection_to_quick_bet_to_which_free_bet_token_is_applied_to_on_market_level_and_repeat_steps_2_5(self):
        """
        DESCRIPTION: Add selection to Quick Bet to which Free bet token is applied to on market level and repeat steps #2-5
        EXPECTED: 
        """
        pass

    def test_007_add_selection_to_quick_bet_to_which_free_bet_token_is_applied_to_on_event_level_and_repeat_steps_2_5(self):
        """
        DESCRIPTION: Add selection to Quick Bet to which Free bet token is applied to on event level and repeat steps #2-5
        EXPECTED: 
        """
        pass

    def test_008_add_selection_to_quick_bet_to_which_free_bet_token_is_applied_to_on_type_level_and_repeat_steps_2_5(self):
        """
        DESCRIPTION: Add selection to Quick Bet to which Free bet token is applied to on type level and repeat steps #2-5
        EXPECTED: 
        """
        pass

    def test_009_add_selection_to_quick_bet_to_which_free_bet_token_is_applied_to_on_class_level_and_repeat_steps_2_5(self):
        """
        DESCRIPTION: Add selection to Quick Bet to which Free bet token is applied to on class level and repeat steps #2-5
        EXPECTED: 
        """
        pass

    def test_010_add_selection_to_quick_bet_to_which_free_bet_token_is_applied_to_on_all_level_and_repeat_steps_2_5(self):
        """
        DESCRIPTION: Add selection to Quick Bet to which Free bet token is applied to on all level and repeat steps #2-5
        EXPECTED: 
        """
        pass
