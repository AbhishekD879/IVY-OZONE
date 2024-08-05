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
class Test_C16379447_Place_a_bet_using_Free_Bet(Common):
    """
    TR_ID: C16379447
    NAME: Place a bet using Free Bet
    DESCRIPTION: This test case verifies Free Bet Placement
    DESCRIPTION: AUTOTEST [C52736087]
    PRECONDITIONS: Instructions how to add Freebet tokens for TEST2/STAGE users or existing PROD users with already granted tokens can be found here: https://confluence.egalacoral.com/display/SPI/How+to+Manually+Add+Freebet+Token+to+Account
    PRECONDITIONS: 1. User is logged in
    PRECONDITIONS: 2. User has Free Bets available on his account
    PRECONDITIONS: 3. User has at least one selection added to the Betslip
    """
    keep_browser_open = True

    def test_001_load_application_and_go_to_the_betslip(self):
        """
        DESCRIPTION: Load application and go to the Betslip
        EXPECTED: Betslip is open
        """
        pass

    def test_002_verify_use_free_bet_link_is_present_under_selection_and_press_on_it(self):
        """
        DESCRIPTION: Verify "Use Free Bet" link is present under selection and press on it
        EXPECTED: Free Bet Pop up is shown with list of Free Bets available
        """
        pass

    def test_003_select_one_of_available_free_bets_from_free_bet_pop_up(self):
        """
        DESCRIPTION: Select one of available Free Bets from Free Bet pop up
        EXPECTED: * Selected Free Bet has radio button marked as selected
        EXPECTED: * 'Add' button is shown
        EXPECTED: Coral:
        EXPECTED: ![](index.php?/attachments/get/58771145)
        EXPECTED: Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/58771175)
        """
        pass

    def test_004_tap_add_button(self):
        """
        DESCRIPTION: Tap 'Add' button
        EXPECTED: * Pop up is closed
        EXPECTED: * "Use Free Bet" link is changed to "- Remove Free Bet" link
        EXPECTED: * Free bet value is shown under 'Stake' field and in 'Total Stake'
        EXPECTED: Coral:
        EXPECTED: ![](index.php?/attachments/get/58771146)
        EXPECTED: Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/58771176)
        """
        pass

    def test_005_verify_estimated_returns_value_when_free_bet_is_selected(self):
        """
        DESCRIPTION: Verify 'Estimated Returns' value when free bet is selected
        EXPECTED: 'Estimated Returns' is calculated based on formula:
        EXPECTED: **Free Bet Value * Odds** - if odds have a fractional format
        EXPECTED: **Free Bet Value * Odds - Free Bet Value** - if odds have a decimal format
        """
        pass

    def test_006_press_on___remove_free_bet_link(self):
        """
        DESCRIPTION: Press on "- Remove Free Bet" link
        EXPECTED: * "- Remove Free Bet" link is changed to "Use Free Bet" link
        EXPECTED: * 'Estimated Returns' is changed to 0.00
        """
        pass

    def test_007_tap_on_use_free_bet_link_one_more_time_and_select_one_of_available_free_bet_in_the_list(self):
        """
        DESCRIPTION: Tap on "Use Free Bet" link one more time and select one of available free bet in the list
        EXPECTED: * Selected Free Bet has radio button marked as selected
        EXPECTED: * 'Add' button is shown
        """
        pass

    def test_008_tap_add_button(self):
        """
        DESCRIPTION: Tap 'Add button
        EXPECTED: * Pop up is closed
        EXPECTED: * "Use Free Bet" link is changed to "- Remove Free Bet" link
        EXPECTED: * 'Estimated Returns' is calculated
        """
        pass

    def test_009_tap_place_bet(self):
        """
        DESCRIPTION: Tap 'Place Bet'
        EXPECTED: * Bet is placed successfully
        EXPECTED: * Bet Receipt is shown
        EXPECTED: * Free bet value is shown in 'Stake' and 'Total Stake' on Bet receipt
        EXPECTED: * User balance is NOT changed
        EXPECTED: Coral:
        EXPECTED: ![](index.php?/attachments/get/58771164)
        EXPECTED: Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/58771179)
        """
        pass

    def test_010_go_to_my_bets__open_betscash_outgo_to_the_bet_that_was_just_placedverify_that_bet_is_shown_with_appropriate_stake_value(self):
        """
        DESCRIPTION: Go to My Bets > Open Bets/Cash out
        DESCRIPTION: Go to the bet that was just placed
        DESCRIPTION: Verify that bet is shown with appropriate Stake Value
        EXPECTED: Placed bet is shown:
        EXPECTED: * Stake value = Free bet value which was selected while placing bet
        EXPECTED: * Appropriate Est. Returns. is shown
        EXPECTED: **Free Bet Value * Odds** - if odds have a fractional format
        EXPECTED: **Free Bet Value * Odds - Free Bet Value** - if odds have a decimal format
        EXPECTED: Coral:
        EXPECTED: ![](index.php?/attachments/get/58771183)
        EXPECTED: Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/58771182)
        """
        pass
